from fastapi.testclient import TestClient
from sqlmodel import Session


def test_create_team(client: TestClient) -> None:
    data = {"name": "Foo Fighters"}
    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_read_item_found(client: TestClient) -> None:
    name = "Los Chapolins"
    data = {"name": name}
    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 201
    team_id = response.json()["id"]
    response = client.get(
        f"/api/team/get/{team_id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == team_id
    assert content["name"] == name


def test_read_item_not_found(client: TestClient) -> None:
    response = client.get(
        f"/api/team/get/1000",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Team not found"


def test_uniqueness_name(client: TestClient) -> None:
    data = {"name": "The Fremen"}
    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 201

    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 409


def test_team_add_request_validation(client: TestClient) -> None:
    data = {"nme": "Harkonnens"}
    response = client.post(
        "/api/team/add",
        json=data,
    )

    assert response.status_code == 422


def test_team_update(client: TestClient) -> None:
    data = {"name": "Atreides"}
    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    team_id = content["id"]
    print(type(team_id))

    updated_data = {"id": team_id, "name": "Dead"}
    response = client.put(f"/api/team/update/{team_id}", json=updated_data)
    assert response.status_code == 200
