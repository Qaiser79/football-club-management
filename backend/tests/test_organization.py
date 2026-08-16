from fastapi.testclient import TestClient
from app.main import app

client= TestClient(app)

def test_get_organizations():
    response = client.get("/organization/")

    assert response.status_code == 200

    data = response.json()

    assert "items" in data
    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "pages" in data

def test_get_organizations_by_name():
    response = client.get("/organization/?name=Ali")

    assert response.status_code == 200

    data = response.json()

    for organization in data["items"]:
        assert "ali" in organization["name"].lower()

def test_get_organizations_pagination():
    response = client.get("/organization/?page=1&limit=1")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 1
    assert len(data["items"]) <= 1

def test_get_organizations_sort_by_name():
    response = client.get("/organization/?sort=name")

    assert response.status_code == 200

    data = response.json()

    names = [organization["name"] for organization in data["items"]]

    assert names == sorted(names)

def test_get_organizations_sort_by_name_desc():
    response = client.get("/organization/?sort=-name")

    assert response.status_code == 200

    data = response.json()

    names = [organization["name"] for organization in data["items"]]

    assert names == sorted(names, reverse=True)

def test_get_organizations_sort_by_created_at():
    response = client.get("/organization/?sort=created_at")

    assert response.status_code == 200

    data = response.json()

    dates = [organization["created_at"] for organization in data["items"]]

    assert dates == sorted(dates)

def test_get_organizations_sort_by_created_at_desc():
    response = client.get("/organization/?sort=-created_at")

    assert response.status_code == 200

    data = response.json()

    dates = [organization["created_at"] for organization in data["items"]]

    assert dates == sorted(dates, reverse=True)

def test_get_organizations_invalid_sort():
    response = client.get("/organization/?sort=banana")

    assert response.status_code == 400

    data = response.json()

    assert data["detail"].lower() == "invalid sort field"

def test_get_organizations_combined_filters():
    initial_response = client.get("/organization/?limit=1")

    assert initial_response.status_code == 200

    initial_data = initial_response.json()

    if not initial_data["items"]:
        return

    organization_name = initial_data["items"][0]["name"]

    response = client.get(
        f"/organization/?name={organization_name}&page=1&limit=1"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["limit"] == 1
    assert len(data["items"]) <= 1

    for organization in data["items"]:
        assert organization_name.lower() in organization["name"].lower()

def test_get_organizations_empty_result():
    response = client.get(
        "/organization/?name=DefinitelyDoesNotExist"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 0
    assert data["pages"] == 0