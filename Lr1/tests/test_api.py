from tests.conftest import register_and_login


def test_register_login_and_me(client):
    headers = register_and_login(client)
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "tatiana"
    assert "hashed_password" not in response.json()


def test_task_crud(client):
    headers = register_and_login(client)
    created = client.post("/tasks", headers=headers, json={"title": "Сделать лабораторную", "priority": "high"})
    assert created.status_code == 201
    task_id = created.json()["id"]
    updated = client.patch(f"/tasks/{task_id}", headers=headers, json={"status": "completed"})
    assert updated.json()["status"] == "completed"
    assert client.delete(f"/tasks/{task_id}", headers=headers).status_code == 204


def test_user_cannot_read_another_users_task(client):
    first = register_and_login(client, "first")
    task_id = client.post("/tasks", headers=first, json={"title": "Секрет"}).json()["id"]
    second = register_and_login(client, "second")
    assert client.get(f"/tasks/{task_id}", headers=second).status_code == 404


def test_many_to_many_and_time_entry(client):
    headers = register_and_login(client)
    task_id = client.post("/tasks", headers=headers, json={"title": "Учёба"}).json()["id"]
    tag_id = client.post("/tags", headers=headers, json={"name": "важно"}).json()["id"]
    task = client.post(f"/tasks/{task_id}/tags/{tag_id}", headers=headers)
    assert task.json()["tags"][0]["name"] == "важно"
    entry = client.post(f"/tasks/{task_id}/time", headers=headers, json={"started_at": "2026-09-20T10:00:00Z", "ended_at": "2026-09-20T11:30:00Z"})
    assert entry.json()["duration_minutes"] == 90

