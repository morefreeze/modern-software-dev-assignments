from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import Note, NoteCreate


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=Note)
def create_note(payload: NoteCreate) -> Note:
    """Create a new note."""
    note_id = db.insert_note(payload.content.strip())
    note = db.get_note(note_id)
    return Note(id=note["id"], content=note["content"], created_at=note["created_at"])


@router.get("/{note_id}", response_model=Note)
def get_single_note(note_id: int) -> Note:
    """Get a single note by ID."""
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return Note(id=row["id"], content=row["content"], created_at=row["created_at"])


@router.get("", response_model=List[Note])
def list_all_notes() -> List[Note]:
    """List all notes in descending order of creation."""
    rows = db.list_notes()
    return [
        Note(id=row["id"], content=row["content"], created_at=row["created_at"])
        for row in rows
    ]


