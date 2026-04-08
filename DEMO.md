# Continuous Learning — Demo & Test Scenarios

Each scenario below includes an **exact prompt** you can paste into an ACP session pointed at this repo. Every prompt is designed to trigger a specific CL behavior and produce a draft PR.

## Prerequisites

1. Workspace has `continuous-learning.enabled` flag ON
2. This repo is cloned as a session repo with `autoPush: true`
3. Session has `gh` CLI and `git` available (standard ACP runner)

---

## Scenario 1: Correction Capture — Wrong Pattern

**What it tests:** Claude does something one way, user corrects to a different way. CL silently captures a correction draft PR.

### Step A — Set up the mistake
```
Add a PATCH /tasks/{task_id} endpoint to update a task's status. Use a plain dict for the request body.
```

### Step B — Correct it
```
No, don't use a plain dict. Create a proper Pydantic model called TaskUpdate with an optional status field. We always use Pydantic models for request bodies in this project.
```

**Expected:** Draft PR on branch `learned/correction-<date>-use-pydantic-models-for-request-bodies` with a file in `docs/learned/corrections/` describing the correction from dict to Pydantic model.

---

## Scenario 2: Correction Capture — Wrong Approach

**What it tests:** Claude uses a sync approach, user redirects to async.

### Step A — Set up the mistake
```
Add a DELETE /tasks/{task_id} endpoint that removes a task from the list.
```

*(Wait for Claude to implement it — if it writes `def delete_task` instead of `async def delete_task`:)*

### Step B — Correct it
```
That needs to be async def, not def. All endpoints in this project are async.
```

**Expected:** Draft PR capturing the correction: sync → async endpoint convention.

---

## Scenario 3: Correction Capture — Wrong File Location

**What it tests:** Claude puts code in the wrong place, user redirects.

### Step A — Set up the mistake
```
Add input validation that rejects task titles containing special characters. Put the validation logic in main.py.
```

### Step B — Correct it
```
Don't put validation in main.py. Use Pydantic field validators in models.py — that's where all validation belongs in this project.
```

**Expected:** Draft PR capturing: validation belongs in models.py via Pydantic validators, not in endpoint handlers.

---

## Scenario 4: Correction Capture — Wrong Error Format

**What it tests:** Claude uses a non-standard error response format.

### Step A — Set up the mistake
```
Update the get_task endpoint to return a better error message when the task isn't found. Include the task_id in the response.
```

*(If Claude returns something like `{"error": "not found", "task_id": "..."}`:)*

### Step B — Correct it
```
No, use HTTPException with the detail field. Our standard error format is {"detail": "Task 'abc' not found"} — FastAPI generates this automatically from HTTPException. Don't build custom error dicts.
```

**Expected:** Draft PR capturing: use HTTPException detail field, not custom error dicts.

---

## Scenario 5: Explicit Capture — Pattern

**What it tests:** User explicitly saves a pattern.

```
save this to learned: In this project, all ID fields use uuid4().hex[:8] for short readable IDs. Don't use auto-incrementing integers or full UUIDs — the short hex format is intentional for human-readability in logs and URLs.
```

**Expected:** Draft PR on branch `learned/pattern-<date>-short-hex-ids` with a file in `docs/learned/patterns/`.

---

## Scenario 6: Explicit Capture — Convention

**What it tests:** User saves a project convention.

```
save this to learned: Every new endpoint must have a corresponding test in tests/test_main.py using FastAPI's TestClient. Tests should cover the happy path, validation errors (422), and not-found cases (404) where applicable.
```

**Expected:** Draft PR capturing the testing convention.

---

## Scenario 7: Explicit Capture — Gotcha

**What it tests:** User saves a non-obvious gotcha.

```
save this to learned: The in-memory _tasks list in main.py resets on every server restart. This is intentional for the demo, but it means tests that depend on state from previous tests will be flaky. Each test should create its own test data.
```

**Expected:** Draft PR capturing the gotcha about in-memory storage and test isolation.

---

## Scenario 8: Explicit Capture — Architecture Decision

**What it tests:** User saves a design rationale.

```
save this to learned: We chose not to add a database for this service because it's a demo/reference implementation. The in-memory list is the simplest thing that works. If someone forks this for production, they should swap _tasks for SQLAlchemy or similar, but the API contract stays the same.
```

**Expected:** Draft PR capturing the architecture decision.

---

## Scenario 9: No Capture — Positive Feedback

**What it tests:** CL does NOT capture when there's no correction.

```
That looks great, exactly what I wanted. Nice work on the error handling.
```

**Expected:** No draft PR created. Positive feedback is not a correction.

---

## Scenario 10: No Capture — Simple Request

**What it tests:** CL does NOT capture simple new requests.

```
Add a GET /tasks/count endpoint that returns the total number of tasks.
```

**Expected:** No draft PR. This is a new request, not a correction or explicit save.

---

## Scenario 11: No Capture — CL Disabled

**What it tests:** Nothing is captured when the feature is off.

*Requires: workspace flag OFF or `.ambient/config.json` removed.*

```
No, use a dataclass instead of Pydantic. We're switching away from Pydantic.
```

**Expected:** No draft PR. CL is not active.

---

## Scenario 12: Wiki Injection

**What it tests:** Compiled wiki is injected into the system prompt.

*Requires: `docs/wiki/INDEX.md` exists in the repo (run wiki compiler first).*

1. Start a new session
2. Ask: `What do you know about this project's conventions from the wiki?`
3. Claude should reference the compiled wiki topics and coverage indicators

**Expected:** Claude's response references wiki articles, not just raw files.

---

## CI Test Script

The scenarios above can be automated as deterministic checks. The following script validates that the CL system prompt instructions are correctly injected:

```bash
#!/bin/bash
# ci-test-cl-prompts.sh — Validates CL prompt injection
# Run from the runner test directory

set -euo pipefail

RUNNER_DIR="components/runners/ambient-runner"

echo "=== Test: CL prompt contains correction capture instructions ==="
cd "$RUNNER_DIR"
python -c "
from ambient_runner.platform.prompts import build_continuous_learning_prompt
prompt = build_continuous_learning_prompt('/repo', 'test-session', 'test-project', 'Test User')
assert 'Correction Capture' in prompt, 'Missing correction capture section'
assert 'learned/correction-' in prompt, 'Missing correction branch pattern'
assert 'gh pr create --draft' in prompt, 'Missing draft PR command'
assert 'Do NOT ask the user' in prompt, 'Missing silence requirement'
print('PASS: Correction capture instructions present')
"

echo "=== Test: CL prompt contains explicit capture instructions ==="
python -c "
from ambient_runner.platform.prompts import build_continuous_learning_prompt
prompt = build_continuous_learning_prompt('/repo', 'test-session', 'test-project', 'Test User')
assert 'Explicit Capture' in prompt, 'Missing explicit capture section'
assert 'save this to learned' in prompt, 'Missing trigger phrase'
assert 'learned/pattern-' in prompt, 'Missing pattern branch pattern'
assert 'Saved to learned knowledge' in prompt, 'Missing acknowledgment'
print('PASS: Explicit capture instructions present')
"

echo "=== Test: CL prompt contains exclusion rules ==="
python -c "
from ambient_runner.platform.prompts import build_continuous_learning_prompt
prompt = build_continuous_learning_prompt('/repo', 'test-session', 'test-project', 'Test User')
assert 'What NOT to Capture' in prompt, 'Missing exclusion section'
assert 'Trivial or temporary' in prompt, 'Missing trivial exclusion'
print('PASS: Exclusion rules present')
"

echo "=== Test: CL prompt substitutes env vars ==="
python -c "
from ambient_runner.platform.prompts import build_continuous_learning_prompt
prompt = build_continuous_learning_prompt('/repo', 'session-xyz', 'my-project', 'Jane Doe')
assert 'session-xyz' in prompt, 'Session ID not substituted'
assert 'my-project' in prompt, 'Project name not substituted'
assert 'Jane Doe' in prompt, 'Author name not substituted'
print('PASS: Env var substitution works')
"

echo "=== Test: Wiki injection with existing INDEX.md ==="
python -c "
import tempfile, os
from ambient_runner.platform.prompts import build_wiki_injection_prompt
with tempfile.TemporaryDirectory() as d:
    idx = os.path.join(d, 'INDEX.md')
    open(idx, 'w').write('# Wiki Index')
    prompt = build_wiki_injection_prompt(idx)
    assert 'coverage' in prompt.lower(), 'Missing coverage instructions'
    assert idx in prompt, 'Wiki path not in prompt'
    print('PASS: Wiki injection works with existing INDEX.md')
"

echo "=== Test: Wiki injection without INDEX.md ==="
python -c "
from ambient_runner.platform.prompts import build_wiki_injection_prompt
prompt = build_wiki_injection_prompt('/nonexistent/docs/wiki/INDEX.md')
assert prompt == '', 'Should return empty string for missing wiki'
print('PASS: Wiki injection gracefully absent')
"

echo "=== Test: Two-gate evaluation ==="
python -c "
from ambient_runner.platform.config import is_continuous_learning_enabled
ok, path = is_continuous_learning_enabled([('/repo', {'learning': {'enabled': True}})], True)
assert ok and path == '/repo', 'Both gates on should enable CL'
ok, path = is_continuous_learning_enabled([('/repo', {'learning': {'enabled': True}})], False)
assert not ok, 'Flag off should disable CL'
ok, path = is_continuous_learning_enabled([('/repo', {'learning': {'enabled': False}})], True)
assert not ok, 'Config off should disable CL'
ok, path = is_continuous_learning_enabled([], True)
assert not ok, 'No repos should disable CL'
print('PASS: Two-gate evaluation works')
"

echo ""
echo "All CI tests passed."
```

## Scenario Matrix

| # | Type | Trigger | Expected Result | PR Branch Pattern |
|---|------|---------|-----------------|-------------------|
| 1 | Correction | Wrong pattern (dict vs Pydantic) | Draft PR | `learned/correction-*` |
| 2 | Correction | Wrong approach (sync vs async) | Draft PR | `learned/correction-*` |
| 3 | Correction | Wrong location (main.py vs models.py) | Draft PR | `learned/correction-*` |
| 4 | Correction | Wrong error format | Draft PR | `learned/correction-*` |
| 5 | Explicit | Pattern (ID format) | Draft PR | `learned/pattern-*` |
| 6 | Explicit | Convention (testing) | Draft PR | `learned/pattern-*` |
| 7 | Explicit | Gotcha (in-memory state) | Draft PR | `learned/pattern-*` |
| 8 | Explicit | Architecture decision | Draft PR | `learned/pattern-*` |
| 9 | Negative | Positive feedback | No PR | — |
| 10 | Negative | Simple request | No PR | — |
| 11 | Negative | CL disabled | No PR | — |
| 12 | Wiki | Wiki injection | Wiki in prompt | — |
