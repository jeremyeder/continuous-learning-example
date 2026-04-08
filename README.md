# Continuous Learning Example

A working example demonstrating the Continuous Learning pipeline for the
[Ambient Code Platform](https://github.com/ambient-code/platform). This
repository is a real, functional Python API service — not a skeleton — with
the full CL wiring in place: config, docs structure, learned knowledge files
submitted as draft PRs, and GitHub Action workflows for wiki compilation.

## What This Demonstrates

1. **`.ambient/config.json`** — repo-level opt-in to Continuous Learning.
2. **`ARCHITECTURE.md`** — bird's-eye codemap following the matklad convention.
3. **`docs/` structure** — human-authored design docs and references alongside
   machine-captured learned knowledge.
4. **`docs/learned/`** — corrections and patterns captured from sessions,
   submitted as draft PRs with the `continuous-learning` label.
5. **`.wiki-compiler.json`** — configuration for compiling the full `docs/`
   tree plus `ARCHITECTURE.md` into a topic-based wiki.
6. **GitHub Action workflows** — both a standalone `workflow_dispatch` workflow
   and an `ambient-action` workflow for automated wiki compilation.

## The API Service

A minimal task management API built with FastAPI:

```
GET  /health        — health check
GET  /tasks         — list all tasks
POST /tasks         — create a task
GET  /tasks/{id}    — get a task by ID
```

Run it:

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

Run tests:

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Enable Continuous Learning on Your Repo

1. Add `.ambient/config.json` to your repo root:
   ```json
   {"learning": {"enabled": true}}
   ```

2. Enable the `continuous-learning.enabled` workspace flag in your ACP project settings.

3. (Optional) Add an `ARCHITECTURE.md` at the repo root describing your codebase structure.

4. (Optional) Add a `.wiki-compiler.json` for standalone wiki compilation, or use the
   `ambient-action` workflow which needs no config file.

That's it. Corrections and patterns will be captured as draft PRs to `docs/learned/`
during sessions. Merge the ones worth keeping; close the rest.

## Prior Art

This feature's design draws from several precedents:

- **[Claude Code Memory](https://code.claude.com/docs/en/memory)** — local
  memory system with markdown files, frontmatter, auto-detection of corrections,
  and session-start injection. Continuous Learning makes this hosted, shared,
  and human-curated via PRs.

- **[Harness Engineering (OpenAI)](https://openai.com/index/harness-engineering/)** —
  the `docs/` directory structure (AGENTS.md, ARCHITECTURE.md, design-docs/,
  references/) as the agent's runtime context. Continuous Learning adopts this
  structure and adds `docs/learned/` as the continuously-captured layer.

- **[ARCHITECTURE.md (matklad)](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)** —
  bird's-eye codemap at the repo root: coarse-grained modules, architectural
  invariants, cross-cutting concerns. Maintained loosely, not on every commit.

- **[LLM Knowledge Base (Karpathy)](https://x.com/karpathy/status/2039805659525644595)** —
  scattered source files compiled by an LLM into a topic-based wiki. Raw data
  becomes compiled knowledge becomes a queryable wiki.

- **[llm-wiki-compiler](https://github.com/ussumant/llm-wiki-compiler)** —
  Claude Code plugin implementing Karpathy's pattern. Compiles markdown sources
  into topic articles with coverage indicators and cross-cutting concept discovery.

- **[Cognee](https://github.com/topoteretes/cognee)** — the framing that most
  bottlenecks in agentic systems are memory problems: continual learning, context
  engineering, and multi-agent coordination all reduce to deciding what to keep,
  how to merge it, and how to reuse it.
