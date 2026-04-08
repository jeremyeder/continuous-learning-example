# API Design Decisions

## Why FastAPI

FastAPI was chosen for the example service for three reasons:

1. **Automatic OpenAPI schema** — every endpoint gets a generated spec with
   zero extra code. This is useful for demonstrating docs-as-code patterns
   alongside Continuous Learning.
2. **Pydantic-native validation** — request bodies are validated against
   Pydantic models before the handler runs. Invalid payloads return 422
   with structured error details automatically.
3. **Async-first** — `async def` handlers are the default. Even though this
   example uses an in-memory list (no I/O), async endpoints keep the door
   open for a database swap without changing signatures.

## Why In-Memory Storage

This is a demonstration codebase. A real service would use a database, but
the in-memory list makes the example self-contained: no migrations, no
connection strings, no Docker Compose. The trade-off (data lost on restart)
is acceptable for an example whose purpose is to show the Continuous
Learning pipeline, not production persistence.

## REST Conventions

- **POST returns 201** with the created resource, not 200.
- **GET returns 200** for success, 404 for missing resources.
- **Validation errors return 422** (FastAPI default via Pydantic).
- **Error bodies use `{"detail": "..."}` format** — FastAPI's `HTTPException`
  default. No custom error envelope.

## Error Handling Approach

Errors are handled with FastAPI's `HTTPException`. There is no global
exception handler or custom middleware. This keeps the example minimal
while still producing consistent error responses.

For a production service, you would add:
- A global exception handler for unexpected errors (500 with a request ID).
- Structured logging of errors with correlation IDs.
- Rate limiting middleware.

None of these are needed for the Continuous Learning demonstration.
