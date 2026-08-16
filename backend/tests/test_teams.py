from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_teams():
    response = client.get("/team/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "pages" in data

def test_get_teams_by_type():
    response = client.get("/team/?team_type=U16")

    assert response.status_code == 200

    data = response.json()

    for team in data["items"]:
        assert team["team_type"].lower() == "u16"

def test_get_teams_by_club():
    response = client.get("/team/?club_id=3")

    assert response.status_code == 200

    data = response.json()

    for team in data["items"]:
        assert team["club_id"] == 3

def test_get_teams_invalid_club():
    response = client.get("/team/?club_id=9999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"].lower() == "club not found"

def test_get_teams_pagination():
    response = client.get("/team/?page=1&limit=1")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 1
    assert len(data["items"]) <= 1

def test_get_teams_sort_by_name():
    response = client.get("/team/?sort=name")

    assert response.status_code == 200

    data = response.json()

    names = [team["name"] for team in data["items"]]

    assert names == sorted(names)

def test_get_teams_sort_by_name_desc():
    response = client.get("/team/?sort=-name")

    assert response.status_code == 200

    data = response.json()

    names = [team["name"] for team in data["items"]]

    assert names == sorted(names, reverse=True)

def test_get_teams_invalid_sort():
    response = client.get("/team/?sort=banana")

    assert response.status_code == 400

    data = response.json()

    assert data["detail"].lower() == "invalid sort field"

def test_get_teams_combined_filters():
    response = client.get(
        "/team/?club_id=3&team_type=U16&page=1&limit=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 1
    assert len(data["items"]) <= 1

    for team in data["items"]:
        assert team["club_id"] == 3
        assert team["team_type"].lower() == "u16"

    
def test_get_teams_empty_result():
    response = client.get("/team/?team_type=DefinitelyDoesNotExist")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["pages"] == 0