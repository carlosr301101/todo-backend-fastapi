from fastapi.testclient import TestClient
from ..app import app

client = TestClient(app)

def get_token(username, password):
    client.post("/auth/register", auth=(username, password))
    response = client.post("/auth/login", auth=(username, password))
    return response.json()["access_token"]

def test_create_task():
    token = get_token("taskuser", "taskpass")
    response = client.post(
        "/api/tasks",
        json={"titulo": "Tarea 1", "descripcion": "Descripción de prueba"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Tarea 1"
    assert data["descripcion"] == "Descripción de prueba"

def test_list_tasks():
    token = get_token("listuser", "listpass")
    client.post(
        "/api/tasks",
        json={"titulo": "Tarea 2", "descripcion": "Otra descripción"},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get(
        "/api/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 1

def test_get_task_by_id():
    token = get_token("getuser", "getpass")
    # Crea una tarea
    create_resp = client.post(
        "/api/tasks",
        json={"titulo": "Tarea 3", "descripcion": "Desc"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_resp.json()["id"]
    # Obtiene la tarea por ID
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id

def test_update_task():
    token = get_token("updateuser", "updatepass")
    create_resp = client.post(
        "/api/tasks",
        json={"titulo": "Tarea 4", "descripcion": "Desc"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_resp.json()["id"]
    # Actualiza la tarea
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"titulo": "Tarea Actualizada"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "Tarea Actualizada"

def test_delete_task():
    token = get_token("deleteuser", "deletepass")
    create_resp = client.post(
        "/api/tasks",
        json={"titulo": "Tarea 5", "descripcion": "Desc"},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_resp.json()["id"]
    # Elimina la tarea
    response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204