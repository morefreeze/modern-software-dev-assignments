from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException

from .. import db
from ..services.extract import extract_action_items, extract_action_items_llm
from ..schemas import (
    ExtractActionItemsRequest,
    ExtractActionItemsResponse,
    ActionItem
)


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractActionItemsResponse)
def extract(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    """Extract action items from text using heuristic method."""
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text.strip())

    items = extract_action_items(payload.text.strip())
    ids = db.insert_action_items(items, note_id=note_id)
    return ExtractActionItemsResponse(
        note_id=note_id,
        items=[{"id": i, "text": t} for i, t in zip(ids, items)]
    )


@router.post("/extract-llm", response_model=ExtractActionItemsResponse)
def extract_llm(payload: ExtractActionItemsRequest):
    """Extract action items from text using LLM method."""
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text.strip())

    items = extract_action_items_llm(payload.text.strip())
    ids = db.insert_action_items(items, note_id=note_id)
    data = {
        "note_id": note_id,
        "items": [{"id": i, "text": t} for i, t in zip(ids, items)]
    }
    print("Data to validate:", data)
    print("Type of first id:", type(data["items"][0]["id"]) if data["items"] else "No items")
    return data


@router.get("", response_model=List[ActionItem])
def list_all(note_id: Optional[int] = None) -> List[ActionItem]:
    """List all action items, optionally filtered by note ID."""
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItem(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done")
def mark_done(action_item_id: int, done: bool = True) -> dict:
    """Mark an action item as done or not done."""
    db.mark_action_item_done(action_item_id, done)
    return {"id": action_item_id, "done": done}


