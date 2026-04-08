"""Pydantic v2 models for the Task API."""

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Possible states for a task."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Request body for creating a task."""

    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)


class Task(BaseModel):
    """A task with server-generated fields."""

    id: str = Field(default_factory=lambda: uuid4().hex[:8])
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
