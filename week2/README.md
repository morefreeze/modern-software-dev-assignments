# Week 2 — Action Item Extractor

A FastAPI application that extracts action items from free-form text using two methods: a heuristic rule-based extractor and an LLM-based extractor powered by Ollama.

## Features

- **Heuristic extraction** — matches bullet points (`-`, `*`, `•`), numbered lists, checkbox markers (`[ ]`), and keyword prefixes (`Todo:`, `Action:`, `Next:`). Falls back to imperative-sentence detection when no structured markers are found.
- **LLM extraction** — sends text to a local `llama3` model via Ollama and parses the response into a clean list of action items.
- **REST API** — FastAPI backend with auto-generated docs at `/docs`.
- **Frontend** — single-page HTML/JS UI served at `/`.

## Requirements

- Python 3.10+
- [Ollama](https://ollama.ai/) running locally with the `llama3` model pulled
- Dependencies managed via Poetry

## Setup

```bash
# Install dependencies
cd week2
poetry install

# Pull the LLM model (one-time)
ollama pull llama3
```

## Running the App

```bash
# From the repo root
poetry run uvicorn week2.app.main:app --reload
```

The app will be available at `http://localhost:8000`.
API docs: `http://localhost:8000/docs`

## API Endpoints

### Notes

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/notes` | Create a new note |
| `GET` | `/notes` | List all notes |
| `GET` | `/notes/{note_id}` | Get a single note by ID |

### Action Items

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/action-items/extract` | Extract action items (heuristic) |
| `POST` | `/action-items/extract-llm` | Extract action items (LLM via Ollama) |
| `GET` | `/action-items` | List all action items |
| `POST` | `/action-items/{id}/done` | Mark an action item as done |

### Request body for extraction endpoints

```json
{
  "text": "- [ ] Set up database\n- Implement API\nTodo: Write tests",
  "save_note": false
}
```

## Running Tests

```bash
cd week2
PYTHONPATH=. poetry run pytest tests/ -v
```

> Note: Tests that call `extract_action_items_llm` require a running Ollama instance with `llama3` pulled. Non-LLM tests run without Ollama.

## Project Structure

```
week2/
├── app/
│   ├── main.py              # FastAPI app, router registration
│   ├── db.py                # SQLite database helpers
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas/
│   │   └── __init__.py      # Pydantic request/response schemas
│   ├── routers/
│   │   ├── notes.py         # /notes endpoints
│   │   └── action_items.py  # /action-items endpoints
│   └── services/
│       └── extract.py       # Heuristic + LLM extraction logic
├── tests/
│   └── test_extract.py      # Unit tests for extraction functions
├── frontend/
│   └── index.html           # Single-page UI
└── data/                    # SQLite database file (auto-created)
```
