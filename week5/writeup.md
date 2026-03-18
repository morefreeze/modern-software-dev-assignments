# Week 5 Write-up
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
### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Use Warp Drive saved prompts and rules to automate the implementation of full Notes CRUD with optimistic UI updates.
> **Saved Prompt:** "Add PUT /notes/{note_id} and DELETE /notes/{note_id} endpoints to the FastAPI backend. Add NoteUpdate Pydantic schema. Update the frontend app.js to add edit (prompt-based) and delete (confirm-based) buttons for each note with optimistic UI updates and error rollback."
> **Rule configured:** "Always use Pydantic schemas for request/response validation. Always add HTTPException 404 for missing resources."
> **Steps:**
> 1. Configured Warp Drive saved prompt with the above specification.
> 2. Ran the saved prompt — Warp generated backend changes (`schemas.py`, `routers/notes.py`) and frontend changes (`frontend/app.js`).
> 3. Verified: `PYTHONPATH=. poetry run pytest backend/tests/ -v` — all tests pass.
> 4. Manually tested UI: create note, edit note (prompt shows current values), delete note (confirm dialog), all UI changes reflected without page reload.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Manually writing PUT/DELETE endpoints requires remembering FastAPI patterns, Pydantic schema definitions, SQLAlchemy update/delete patterns, and then writing matching frontend JS with fetch + error handling — typically 30+ minutes.
> **After:** Single saved Warp prompt generates all backend and frontend changes in under 3 minutes, with correct patterns and error handling included.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> Used **high autonomy** — gave Warp permission to create and edit files in `backend/app/` and `frontend/`. Supervised by running the test suite after generation and manually testing the UI in the browser. No rollback was needed; generated code was correct on first pass.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> Not applicable for this automation — single-agent approach was sufficient for this scoped task.

e. How you used the automation (what pain point it resolves or accelerates)
> This resolved the pain of writing repetitive CRUD boilerplate. Every FastAPI CRUD endpoint follows the same pattern (schema → route → ORM call → 404 check → return), and Warp's saved prompt handles all of that automatically. The optimistic UI update pattern is also boilerplate-heavy on the frontend — the automation eliminated the need to manually write fetch + rollback logic.


### Automation B: Multi‑agent workflows in Warp

a. Design of each automation, including goals, inputs/outputs, steps
> **Goal:** Use a multi-agent workflow in Warp to implement and verify the full CRUD feature in parallel — one agent for backend, one for frontend, one for tests.
> **Agent roles:**
> - **Backend Agent:** Implement `NoteUpdate` schema and `PUT`/`DELETE` endpoints in `backend/app/routers/notes.py` and `backend/app/schemas.py`.
> - **Frontend Agent:** Add edit and delete UI functionality to `frontend/app.js` using the new endpoints.
> - **Test Agent:** Add/update pytest tests in `backend/tests/` to cover the new endpoints.
> **Coordination:** Backend agent ran first (its output defines the API contract). Frontend and Test agents ran in parallel after the backend was complete.
> **Steps:**
> 1. Ran Backend Agent with spec for PUT/DELETE endpoints.
> 2. After backend complete, ran Frontend Agent and Test Agent in parallel.
> 3. Final verification: `PYTHONPATH=. poetry run pytest backend/tests/ -v` — all tests pass.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> **Before:** Sequential development — write backend, write frontend, write tests, debug conflicts. Each step blocks the next.
> **After:** Backend defines the contract; frontend and tests are generated concurrently, cutting total wall-clock time roughly in half.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> - Backend Agent: **High autonomy** — file create/edit in `backend/app/`. Supervised by reviewing diff before committing.
> - Frontend Agent: **High autonomy** — file edit in `frontend/`. Supervised by manual browser test.
> - Test Agent: **High autonomy** — file create/edit in `backend/tests/`. Supervised by running pytest.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> **Concurrency win:** Frontend and Test agents ran in parallel, saving ~10 minutes.
> **Risk:** If Backend Agent changed the API shape, Frontend and Test agents could generate mismatched code. Mitigated by running Backend Agent first and waiting for it to complete before launching the other two.
> **Failure observed:** None — the parallel agents produced compatible code on first run.

e. How you used the automation (what pain point it resolves or accelerates)
> The multi-agent workflow eliminates the sequential bottleneck in feature development. Writing tests is typically deferred until after the feature is "done", leading to gaps. With this workflow, tests are generated concurrently with the frontend — both are ready at the same time as the backend, so the feature ships with full coverage from the start.

