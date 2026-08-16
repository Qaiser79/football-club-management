from fastapi.testclient import TestClient
from app.main import app
client =TestClient(app)

def test_get_clubs():
    response = client.get("/club/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "pages" in data

def test_get_clubs_by_name():
    response = client.get("/club/?name=Ali")

    assert response.status_code == 200

    data = response.json()

    for club in data["items"]:
        assert "ali" in club["name"].lower()

def test_get_clubs_by_organization():
    response = client.get("/club/?organization_id=1")

    assert response.status_code == 200

    data = response.json()

    for club in data["items"]:
        assert club["organization_id"] == 1

def test_get_clubs_invalid_organization():
    response = client.get("/club/?organization_id=9999")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"].lower() == "organization not found"

def test_get_clubs_pagination():
    response = client.get("/club/?page=1&limit=1")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 1
    assert len(data["items"]) <= 1

def test_get_clubs_sort_by_name():
    response = client.get("/club/?sort=name")

    assert response.status_code == 200

    data = response.json()

    names = [club["name"] for club in data["items"]]

    assert names == sorted(names)

def test_get_clubs_sort_by_name_desc():
    response = client.get("/club/?sort=-name")

    assert response.status_code == 200

    data = response.json()

    names = [club["name"] for club in data["items"]]

    assert names == sorted(names, reverse=True)

def test_get_clubs_invalid_sort():
    response = client.get("/club/?sort=banana")

    assert response.status_code == 400

    data = response.json()

    assert data["detail"].lower() == "invalid sort field"

def test_get_clubs_combined_filters():
    response = client.get(
        "/club/?organization_id=1&page=1&limit=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 1
    assert len(data["items"]) <= 1

    for club in data["items"]:
        assert club["organization_id"] == 1
    
def test_get_clubs_empty_result():
    response = client.get("/club/?name=DefinitelyDoesNotExist")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["pages"] == 0