# FastAPI Patterns Used

## Pydantic v2 Models

Models use Pydantic v2 conventions exclusively:
- `Field(default_factory=...)` for mutable defaults (UUIDs, timestamps).
- `Field(min_length=1)` for input validation.
- `str` enums for automatic JSON serialization.
- No `orm_mode`, no `.dict()` — these are v1 patterns.

## Async Endpoints

All route handlers use `async def`. FastAPI runs sync handlers in a
thread pool, but async handlers run directly on the event loop. Using
async consistently avoids accidental thread-pool exhaustion if the
service later adds real I/O (database queries, HTTP calls).

## TestClient

`fastapi.testclient.TestClient` wraps the ASGI app in a synchronous
HTTP client (backed by `httpx`). Tests are plain `pytest` functions —
no async fixtures or `pytest-asyncio` needed.

The `autouse` fixture clears the in-memory store between tests so
ordering never matters.

## Dependency Injection

FastAPI's `Depends()` system is not used in this example because the
service has no shared dependencies (no database session, no auth).
In a larger service, you would inject a database session via
`Depends(get_db)` and mock it in tests.

## Input/Output Model Separation

`TaskCreate` (input) has only the fields the client controls: `title`
and `description`. `Task` (output) adds server-generated fields: `id`,
`status`, `created_at`. This prevents clients from setting IDs or
timestamps via the request body.
