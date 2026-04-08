---
type: correction
date: 2026-04-01T14:22:00Z
session: task-api-setup-001
project: task-api
author: Jeremy Eder
title: "Use Pydantic v2 model patterns, not v1"
---

## What Happened

When generating `src/models.py`, the agent used Pydantic v1 patterns:
`Field(default=None)` for optional fields, `class Config: orm_mode = True`,
and `.dict()` calls in tests. The `created_at` field used
`Field(default_factory=datetime.utcnow)` which is deprecated in Python 3.12+.

## The Correction

The user pointed out that this project uses Pydantic v2 exclusively:

- Use `Field(default_factory=lambda: datetime.now(timezone.utc))` instead
  of `datetime.utcnow` (deprecated, returns naive datetime).
- Remove `class Config: orm_mode = True` — use `model_config` dict if needed.
- Use `.model_dump()` instead of `.dict()`.
- Use `model_validator` for cross-field validation, not root validators.

## Why It Matters

Pydantic v2 is a ground-up rewrite with different APIs. Mixing v1 and v2
patterns causes subtle bugs: `.dict()` still works but is deprecated and
will be removed, `orm_mode` is silently ignored in v2 `ConfigDict`, and
naive datetimes from `utcnow()` cause timezone comparison failures. The
codebase should be consistently v2 from the start.
