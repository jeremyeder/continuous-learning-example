"""Task Management API — a minimal FastAPI service for demonstrating Continuous Learning."""

from fastapi import FastAPI, HTTPException

from .models import Task, TaskCreate

app = FastAPI(title="Task API", version="0.1.0")

# In-memory store — replaced by a real database in production.
_tasks: list[Task] = []


@app.get("/health")
async def health() -> dict:
    """Return service health status."""
    return {"status": "healthy", "version": app.version}


@app.get("/tasks")
async def list_tasks() -> list[Task]:
    """Return all tasks."""
    return _tasks


@app.post("/tasks", status_code=201)
async def create_task(body: TaskCreate) -> Task:
    """Create a new task and return it."""
    task = Task(title=body.title, description=body.description)
    _tasks.append(task)
    return task


@app.get("/tasks/{task_id}")
async def get_task(task_id: str) -> Task:
    """Return a single task by ID."""
    for task in _tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id!r} not found")
