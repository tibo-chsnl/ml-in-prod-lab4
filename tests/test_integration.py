import pytest
from app import create_app
from extensions import db
from models import User, Task

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_and_login(client):
    response = client.post("/register", data={
        "username": "integration_user",
        "password": "password123",
        "confirm": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful" in response.data

    response = client.post("/login", data={
        "username": "integration_user",
        "password": "password123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data

def test_create_task(client):
    client.post("/register", data={"username": "task_user", "password": "p", "confirm": "p"})
    client.post("/login", data={"username": "task_user", "password": "p"})

    response = client.post("/tasks/new", data={
        "title": "Integration Task",
        "description": "Testing creation",
        "due_date": "2025-12-31"
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Task created" in response.data
    assert b"Integration Task" in response.data

def test_edit_and_toggle_task(client, app):
    client.post("/register", data={"username": "edit_user", "password": "p", "confirm": "p"})
    client.post("/login", data={"username": "edit_user", "password": "p"})
    client.post("/tasks/new", data={"title": "Original Title", "due_date": "2025-01-01"})

    with app.app_context():
        task = Task.query.filter_by(title="Original Title").first()
        assert task is not None
        task_id = task.id
    response = client.post(f"/tasks/{task_id}/edit", data={
        "title": "Updated Title",
        "description": "Updated Desc",
        "due_date": "2025-01-02",
        "is_completed": "" 
    }, follow_redirects=True)
    assert b"Task updated" in response.data
    assert b"Updated Title" in response.data

    response = client.post(f"/tasks/{task_id}/toggle", follow_redirects=True)
    assert b"Task status updated" in response.data

    with app.app_context():
        task = Task.query.get(task_id)
        assert task.is_completed
