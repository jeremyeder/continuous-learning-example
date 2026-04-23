---
type: correction
date: 2026-04-03T09:15:00Z
session: task-api-endpoints-003
project: task-api
author: Jeremy Eder
title: "Use async def for all endpoint handlers"
---

## What Happened

The agent wrote endpoint handlers as plain `def` functions:

```python
@app.get("/tasks")
def list_tasks():
    return _tasks
```

This works, but FastAPI runs sync handlers in a thread pool via
`anyio.to_thread.run_sync`. With an in-memory store this is harmless,
but it sets a bad precedent.

## The Correction

The user asked for all handlers to use `async def` for consistency:

```python
@app.get("/tasks")
async def list_tasks():
    return _tasks
```

Even though the in-memory store has no real I/O, using `async def`
everywhere avoids a future mistake: if someone adds a database call
inside a sync handler, it blocks the thread pool instead of yielding
to the event loop.

## Why It Matters

Consistency prevents accidental performance degradation. When all
handlers are async, adding an `await db.fetch()` call is natural. When
some handlers are sync, a developer might add a blocking call inside a
sync handler without realizing it starves the thread pool. Start async,
stay async.
