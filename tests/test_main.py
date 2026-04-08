"""Tests for the Task API endpoints."""

import pytest
from fastapi.testclient import TestClient

from src.main import app, _tasks


@pytest.fixture(autouse=True)
def _clear_tasks():
    """Reset in-memory store between tests."""
    _tasks.clear()
    yield
    _tasks.clear()


@pytest.fixture
def client():
    return TestClient(app)


# --- GET /health ---


def test_health_returns_200(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "healthy"
    assert "version" in body


# --- POST /tasks ---


def test_create_task_returns_201(client):
    resp = client.post("/tasks", json={"title": "Write docs"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Write docs"
    assert body["status"] == "todo"
    assert "id" in body
    assert "created_at" in body


def test_create_task_with_description(client):
    resp = client.post(
        "/tasks",
        json={"title": "Deploy", "description": "Ship to staging"},
    )
    assert resp.status_code == 201
    assert resp.json()["description"] == "Ship to staging"


def test_create_task_empty_title_returns_422(client):
    resp = client.post("/tasks", json={"title": ""})
    assert resp.status_code == 422


# --- GET /tasks ---


def test_list_tasks_empty(client):
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_tasks_after_create(client):
    client.post("/tasks", json={"title": "A"})
    client.post("/tasks", json={"title": "B"})
    resp = client.get("/tasks")
    assert len(resp.json()) == 2


# --- GET /tasks/{task_id} ---


def test_get_task_by_id(client):
    create_resp = client.post("/tasks", json={"title": "Find me"})
    task_id = create_resp.json()["id"]
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Find me"


def test_get_task_not_found(client):
    resp = client.get("/tasks/nonexistent")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
