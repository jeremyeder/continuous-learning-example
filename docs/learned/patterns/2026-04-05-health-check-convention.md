---
type: pattern
date: 2026-04-05T11:30:00Z
session: task-api-deploy-004
project: task-api
author: Jeremy Eder
title: "Health check endpoint convention"
---

## Pattern

The health check endpoint returns a JSON body with `status` and `version`:

```json
{
  "status": "healthy",
  "version": "0.1.0"
}
```

It always returns HTTP 200. If the service is unhealthy, it should not be
running (let the process crash and let the orchestrator restart it).

## When to Use

Every service in this project must expose `GET /health` with this exact
response shape. Kubernetes liveness and readiness probes point here.

## Why This Convention

- **`status`** is a string, not a boolean, so it can be extended to
  `"degraded"` later without breaking clients that check for `"healthy"`.
- **`version`** comes from `app.version` so it is always in sync with the
  FastAPI app definition. No separate version file to maintain.
- **No dependency checks** in the health endpoint. Database connectivity,
  cache availability, etc. belong in a separate `/ready` endpoint if needed.
  The health check should be fast and side-effect-free.
