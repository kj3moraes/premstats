from fastapi.testclient import TestClient
from sqlmodel import Session


def test_team_create(client: TestClient) -> None:
    data = {"name": "Foo Fighters"}
    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_team_read_item_found(client: TestClient) -> None:
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


def test_team_read_item_not_found(client: TestClient) -> None:
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

    new_name = "Dead"
    updated_data = {"id": team_id, "name": new_name}
    response = client.put(f"/api/team/update/{team_id}", json=updated_data)
    assert response.status_code == 200

    response = client.get(
        f"/api/team/get/{team_id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == new_name


def test_team_update_validation_error(client: TestClient):
    data = {"name": "Duncan Idaho"}
    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    team_id = content["id"]

    new_name = "Duncan Ghola"
    updated_data = {"id": team_id, "new_name": new_name}
    response = client.put(f"/api/team/update/{team_id}", json=updated_data)
    assert response.status_code == 422


def test_team_update_non_existent(client: TestClient) -> None:
    data = {"name": "Buchannan"}
    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 201
    content = response.json()

    new_name = "Muerta"
    updated_data = {"name": new_name}
    response = client.put(f"/api/team/update/900000", json=updated_data)
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Team not found"


def test_team_delete(client: TestClient) -> None:
    data = {"name": "Feyd Rautha"}
    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 201
    content = response.json()
    team_id = content["id"]

    response = client.delete(f"/api/team/delete/{team_id}")
    assert response.status_code == 204
    response = client.get(
        f"/api/team/get/{team_id}",
    )
    assert response.status_code == 404


def test_team_delete_non_existent(client: TestClient) -> None:
    data = {"name": "Na-baron"}
    response = client.post(
        "/api/team/add",
        json=data,
    )
    assert response.status_code == 201

    response = client.delete(f"/api/team/delete/12345678")
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Team not found"
