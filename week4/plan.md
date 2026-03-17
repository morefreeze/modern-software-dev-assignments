# Week 4 - Full Stack Application: Build Notes API

## [x] 1. Requirements Recap

Week4 assignment: Build a full-stack notes application with:
- Backend: FastAPI + SQLAlchemy + SQLite
- Frontend: Simple HTML/JS (or reuse existing from template)
- Features:
  - [x] Create notes
  - [x] List notes
  - [x] Get single note
  - [x] Update notes
  - [x] Delete notes
  - [x] Extract action items from note content using LLM
  - [x] All the above with proper tests

## [x] 2. Implementation Summary

**Backend structure already created:**
- `week4/backend/app/`
  - `db.py` - database setup with SQLAlchemy
  - `models.py` - Note model
  - `schemas.py` - Pydantic schemas for request/response
  - `main.py` - FastAPI app with CORS configured
  - `routers/`
    - `notes.py` - CRUD endpoints for notes
    - `action_items.py` - Extract action items endpoint
  - `services/extract.py` - LLM extraction via Ollama
  - `tests/` - pytest tests for all endpoints

## [x] 3. Key Points

- **Database:** SQLite database created via SQLAlchemy ORM
- **REST API:** All CRUD operations proper status codes:
  - `GET /notes` - list all
  - `GET /notes/{id}` - get one
  - `POST /notes` - create
  - `PUT /notes/{id}` - update
  - `DELETE /notes/{id}` - delete
  - `POST /notes/{id}/extract-action-items` - extract action items via LLM

- **LLLM Extraction:** Uses Ollama `llama3` to extract action items from free text notes, same approach as week2

- **Tests:** All endpoints have pytest tests with httpx client for integration testing

## [x] 4. Already Completed

- [x] Database schema and models
- [x] All CRUD routes implemented
- [x] Action item extraction service
- [x] Test suite with all endpoints covered
- [x] FastAPI app configuration
- [x] CORS configured for frontend

## Summary

| Requirement | Status |
|-------------|--------|
| Full-stack notes app | ✅ Done |
| CRUD operations | ✅ Done |
| Action item extraction | ✅ Done |
| Backend tests | ✅ Done |
| Documentation (`plan.md`) | ✅ Done |

All requirements are satisfied. The application is ready to run with `poetry run uvicorn week4.backend.app.main:app --reload`.
