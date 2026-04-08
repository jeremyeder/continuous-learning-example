---
type: pattern
date: 2026-04-02T16:45:00Z
session: task-api-errors-002
project: task-api
author: Jeremy Eder
title: "Standardized error response format"
---

## Pattern

All error responses from the API follow FastAPI's default `HTTPException`
format:

```json
{
  "detail": "Human-readable error message"
}
```

The HTTP status code is set on the response, not duplicated in the body.

## When to Use

- **404** — resource not found. Detail includes the resource type and ID.
- **422** — validation error. FastAPI generates this automatically from
  Pydantic validation failures. The body includes field-level error details.
- **500** — unexpected server error. Not explicitly raised; only occurs if
  an unhandled exception escapes a handler.

## Why This Convention

FastAPI's built-in `HTTPException` already produces `{"detail": "..."}`.
Wrapping it in a custom envelope (`{"error": {"code": ..., "message": ...}}`)
adds complexity without value for a small API. Clients can rely on the HTTP
status code for the error category and `detail` for the human-readable
message.

For larger APIs with multiple error codes per status, a custom error model
would make sense. For this service, the default is sufficient.
