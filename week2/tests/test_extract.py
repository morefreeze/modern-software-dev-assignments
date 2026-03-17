import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_basic():
    """Test LLM extraction with basic action items."""
    text = """
    Meeting notes:
    - [ ] Set up database
    - Implement API extract endpoint
    - Write tests
    """.strip()

    items = extract_action_items_llm(text)
    assert len(items) > 0
    # Check that at least some expected items are present
    found_items = [item.lower() for item in items]
    assert any("database" in item for item in found_items)
    assert any("api" in item for item in found_items)
    assert any("test" in item for item in found_items)


def test_extract_action_items_llm_empty_input():
    """Test LLM extraction with empty input."""
    items = extract_action_items_llm("")
    assert items == []


def test_extract_action_items_llm_no_action_items():
    """Test LLM extraction with text that has no action items."""
    text = "The weather is nice today. I went for a walk in the park. The birds are singing."
    items = extract_action_items_llm(text)
    assert items == []


def test_extract_action_items_llm_keyword_prefixed():
    """Test LLM extraction with keyword-prefixed lines."""
    text = """
    Todo: Fix the login bug
    Action: Update the documentation
    Next: Deploy to production
    """.strip()

    items = extract_action_items_llm(text)
    assert len(items) > 0
    found_items = [item.lower() for item in items]
    assert any("login" in item for item in found_items)
    assert any("documentation" in item for item in found_items)
    assert any("deploy" in item for item in found_items)
