from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def extract_action_items_llm(text: str) -> List[str]:
    """Extract action items using LLM via Ollama with structured output."""
    if not text.strip():
        return []
    try:
        response = chat(
            model="llama3",
            messages=[
                {
                    "role": "system",
                    "content": """Extract action items from the text. Each action item should be on its own line. Do not include any other text. If there are no action items, return nothing. Example input: "Meeting notes: - [ ] Set up database - Implement API extract endpoint - Write tests" Example output: Set up database\nImplement API extract endpoint\nWrite tests"""
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )
        content = response["message"]["content"]
        # Split by lines and clean
        items = []
        seen = set()
        for line in content.strip().splitlines():
            stripped = line.strip()
            if (stripped and
                stripped.lower() not in seen and
                len(stripped) > 3 and
                not stripped.startswith("(") and
                not stripped.startswith("please") and
                "nothing to extract" not in stripped.lower() and
                "no action items" not in stripped.lower()):
                seen.add(stripped.lower())
                items.append(stripped)
        return items
    except Exception as e:
        print(f"Error extracting action items with LLM: {e}")
        return []


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
