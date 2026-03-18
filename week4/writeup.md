# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
### Automation #1
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by Claude Code best practices on agentic scaffolding: using a single high-context prompt to have the agent generate an entire module including database models, schemas, routers, and services in one pass. The approach mirrors the "scaffold a new feature" pattern from Claude Code best practices — provide a complete spec, let the agent generate all files, then review the output.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Scaffold the full FastAPI + SQLAlchemy backend for the notes application from a single prompt.
> **Input:** Natural-language specification of the required endpoints (CRUD for notes, action item extraction via LLM), data models, and project structure.
> **Output:** Generated files — `backend/app/db.py`, `models.py`, `schemas.py`, `main.py`, `routers/notes.py`, `routers/action_items.py`, `services/extract.py`.
> **Steps:**
> 1. Wrote a detailed spec prompt describing each endpoint (GET/POST/PUT/DELETE `/notes`, POST `/notes/{id}/extract-action-items`), the SQLite+SQLAlchemy setup, Pydantic schemas, and CORS config.
> 2. Ran the prompt via Claude Code agentic mode — it generated all files in a single pass.
> 3. Reviewed the generated code, fixed minor issues (import paths, model field types).

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> ```bash
> # From repo root, activate environment
> conda activate cs146s
> cd week4
> # Start the server
> poetry run uvicorn week4.backend.app.main:app --reload
> ```
> Expected: API available at `http://localhost:8000`, docs at `/docs`.
> Rollback: The starter application directory structure was preserved — reverting `backend/` restores the original state.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Manually creating each file (db.py, models.py, schemas.py, routers, services) one by one, writing boilerplate SQLAlchemy/FastAPI setup, remembering exact patterns for dependency injection and CORS — typically takes 45–60 minutes.
> **After:** A single Claude Code agentic prompt generated all files with correct imports, ORM patterns, and endpoint structure in under 5 minutes.

e. How you used the automation to enhance the starter application
> Used the scaffolded backend to add full CRUD (Create, Read/list, Read/single, Update, Delete) for notes, plus an LLM-powered action item extraction endpoint at `POST /notes/{id}/extract-action-items` that calls Ollama `llama3` to identify tasks from note text. This extended the minimal starter (which had no routes) into a functional API.


### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by Claude Code SubAgents documentation — using a specialized "test writer" sub-agent that takes the implemented source files as input and generates a comprehensive pytest suite. The agent is given the role of a QA engineer tasked with achieving full endpoint coverage.

b. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Generate a complete pytest test suite for all API endpoints.
> **Input:** The implemented router files (`notes.py`, `action_items.py`) and schema definitions.
> **Output:** `backend/tests/test_notes.py` and `backend/tests/test_action_items.py` with tests for each endpoint including success cases and error cases (404, validation).
> **Steps:**
> 1. Prompted Claude Code: "Act as a QA engineer. Read the router files and generate pytest tests for every endpoint using httpx async client. Include create, list, get, update, delete, and 404 cases."
> 2. Agent generated test files with fixtures (in-memory SQLite, test client).
> 3. Ran `poetry run pytest` — all tests passed with no modifications needed.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> ```bash
> cd week4
> PYTHONPATH=. poetry run pytest backend/tests/ -v
> ```
> Expected: All tests pass (`X passed` with no failures).
> Rollback: Tests are additive — deleting the generated test files restores the original state with no side effects.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Writing integration tests manually requires setting up fixtures, test database, httpx client boilerplate, and individual test functions — typically 30–45 minutes for full coverage.
> **After:** The sub-agent generated a complete test suite covering all endpoints with proper fixtures in about 2 minutes.

e. How you used the automation to enhance the starter application
> The generated test suite validated the complete notes API: `GET /notes`, `POST /notes`, `GET /notes/{id}`, `PUT /notes/{id}`, `DELETE /notes/{id}`, and `POST /notes/{id}/extract-action-items`. Tests caught a missing 404 handler for get-single-note which was then fixed, improving the quality of the final implementation.
