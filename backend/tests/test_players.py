from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get_players():
    response = client.get("/player/")

    assert response.status_code ==200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "pages" in data

def test_get_players_pagination():
    response = client.get("/player/?page=1&limit=1")

    assert response.status_code == 200
    data = response.json()

    assert data["page"]==1
    assert data["limit"]==1
    assert len(data["items"])<=1

def test_get_players_by_position():
    response = client.get("/player/?position==Attack")

    assert response.status_code==200

    data = response.json()
    for player in data["items"]:
        assert player["position"].lower()=="attack"

def test_get_players_by_name():
    response = client.get("/player/?name=Ali")

    assert response.status_code == 200

    data = response.json()

    for player in data["items"]:
        assert "ali" in player["name"].lower()

def test_get_players_by_team():
    response = client.get("/player/?team_id=3")

    assert response.status_code == 200

    data = response.json()

    for player in data["items"]:
        assert player["team_id"] == 3

def test_get_players_invalid_team():
    response = client.get("/player/?team_id=9999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"].lower() == "team not found"

def test_get_players_sort_by_name():
    response = client.get("/player/?sort=name")

    assert response.status_code == 200

    data = response.json()

    names = [player["name"] for player in data["items"]]

    assert names == sorted(names)

def test_get_players_sort_by_created_at_desc():
    response = client.get("/player/?sort=-created_at")

    assert response.status_code == 200

    data = response.json()

    dates = [player["created_at"] for player in data["items"]]

    assert dates == sorted(dates, reverse=True)

def test_get_players_invalid_sort():
    response = client.get("/player/?sort=banana")

    assert response.status_code == 400

    data = response.json()

    assert data["detail"].lower() == "invalid sort field"

def test_get_players_combined_filters():
    response = client.get(
        "/player/?team_id=3&position=Attack&page=1&limit=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 1
    assert len(data["items"]) <= 1

    for player in data["items"]:
        assert player["team_id"] == 3
        assert player["position"].lower() == "attack"

def test_get_players_empty_result():
    response = client.get("/player/?name=DefinitelyDoesNotExist")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["pages"] == 0

def test_get_players_page_beyond_results():
    response = client.get("/player/?page=999&limit=10")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["page"] == 999
    assert data["limit"] == 10