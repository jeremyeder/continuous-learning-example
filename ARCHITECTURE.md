# Architecture

A minimal task management API built with FastAPI. This document provides the
bird's-eye view of the codebase following the
[matklad convention](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html).

## Modules

### `src/main.py`
Application entry point. Defines the FastAPI `app` instance and all route
handlers. Tasks are stored in an in-memory list (`_tasks`). No database
dependency — the list is reset on restart.

**Endpoints:**
- `GET  /health`       — returns `{"status": "healthy", "version": "..."}`.
- `GET  /tasks`        — returns the full task list.
- `POST /tasks`        — creates a task from a `TaskCreate` body, returns 201.
- `GET  /tasks/{id}`   — returns a single task or 404.

### `src/models.py`
Pydantic v2 models. `TaskCreate` is the inbound request body (title +
optional description). `Task` adds server-generated fields: `id` (short
UUID), `status` (enum: todo / in_progress / done), and `created_at` (UTC
timestamp). `TaskStatus` is a `str` enum so JSON serialization is automatic.

## Data Flow

```
Client request
  -> FastAPI route handler (src/main.py)
  -> Pydantic validation (src/models.py)
  -> In-memory list (_tasks)
  -> JSON response
```

## Key Patterns

- **Pydantic v2** — `model_validator`, `Field(default_factory=...)`, native
  `datetime` with timezone. No v1 compatibility shims.
- **Async endpoints** — all handlers are `async def` for consistency even
  though the in-memory store is synchronous.
- **Separation of input/output models** — `TaskCreate` (input) vs `Task`
  (output) prevents clients from setting server-generated fields.
- **TestClient tests** — `fastapi.testclient.TestClient` with an autouse
  fixture that clears `_tasks` between tests.
