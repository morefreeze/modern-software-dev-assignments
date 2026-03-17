from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    """Schema for creating a new note."""
    content: str = Field(..., min_length=1, description="The content of the note")


class Note(BaseModel):
    """Schema for representing a note."""
    id: int
    content: str
    created_at: str

    class Config:
        orm_mode = True


class ActionItem(BaseModel):
    """Schema for representing an action item."""
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str

    class Config:
        orm_mode = True


class ExtractActionItemsRequest(BaseModel):
    """Schema for extracting action items from text."""
    text: str = Field(..., min_length=1, description="The text to extract action items from")
    save_note: bool = Field(False, description="Whether to save the text as a note")


class ActionItemCreate(BaseModel):
    """Schema for representing an action item in extraction response."""
    id: int
    text: str


class ExtractActionItemsResponse(BaseModel):
    """Schema for the response of action item extraction."""
    note_id: Optional[int]
    items: list[ActionItemCreate]