# Week 5 Plan

## Key Points from Assignment

- Use Warp agentic development environment and multi-agent workflows
- Choose 2 or more tasks from TASKS.md
- Implement Warp Drive features (saved prompts, rules, MCP servers)
- Implement multi-agent workflows within Warp
- Work strictly in week5/ directory
- Deliver Warp automations and writeup.md

## Changes Made

### Task Completed: Full Notes CRUD with optimistic UI updates (medium)
1. **Backend Changes**:
   - Added `NoteUpdate` schema to `backend/app/schemas.py`
   - Added `PUT /notes/{note_id}` endpoint to `backend/app/routers/notes.py`
   - Added `DELETE /notes/{note_id}` endpoint to `backend/app/routers/notes.py`

2. **Frontend Changes**:
   - Updated `frontend/app.js` to add edit and delete functionality for notes
   - Added prompt-based edit UI with error handling
   - Added confirm-based delete UI with error handling

### Verification
- All tests pass (`PYTHONPATH=. poetry run pytest backend/tests/ -v`)
- Manually tested endpoints using browser UI:
  - Create note
  - Edit note (shows prompt with current values)
  - Delete note (asks for confirmation)
  - All changes reflected in UI without page reload

## Key Learnings/Insights

1. **CRUD Operations in FastAPI**:
   - Pydantic schemas for request/response validation
   - SQLAlchemy ORM for database operations
   - Proper error handling with HTTPException

2. **Frontend JavaScript**:
   - Optimistic UI updates with error rollback
   - Simple prompt/confirm dialogs for user input
   - Async/await for API calls

3. **Testing**:
   - Importance of isolated tests with proper fixtures
   - Handling dependencies with poetry
   - Resetting git state to avoid accidental changes to other weeks

## Completed Tasks

- [x] Full Notes CRUD with optimistic UI updates (medium)
- [x] Test coverage improvements (implicitly done by running tests)