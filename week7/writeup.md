# Week 7 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## Task 1: Add more endpoints and validations
a. Links to relevant commits/issues
> TODO (PR link)

b. PR Description
> **Problem:** The starter application lacked pagination, sorting, filtering, and proper 404 handling for notes and action items.
>
> **Approach:** Used Claude Code to implement the following additions to `backend/app/routers/`:
> - `GET /notes` — added `skip`, `limit`, `sort_by`, `order` query parameters with validation
> - `GET /notes/{note_id}` — added 404 HTTPException when note not found
> - `GET /action-items` — added `note_id` filter, `skip`/`limit` pagination
> - `POST /action-items/{id}/done` — added toggle endpoint
>
> **Testing:** All existing tests pass; added pagination and filter tests.
>
> **Tradeoffs:** Used simple query-parameter sorting rather than a more flexible cursor-based pagination, which is sufficient for the assignment scope.

c. Graphite Diamond generated code review
> TODO (Graphite AI review)

## Task 2: Extend extraction logic
a. Links to relevant commits/issues
> TODO (PR link)

b. PR Description
> **Problem:** The original `extract_action_items` heuristic only matched bullets/checkboxes and keyword prefixes. It missed imperative sentences and had no fallback.
>
> **Approach:** Extended `backend/app/services/extract.py`:
> - Added `_looks_imperative()` helper that checks if a sentence starts with a known imperative verb (add, create, implement, fix, update, write, check, verify, refactor, document, design, investigate)
> - Added fallback: if no bullet/keyword lines found, split text into sentences and pick imperative-looking ones
> - Added deduplication (case-insensitive) while preserving order
>
> **Testing:** All extraction tests pass including the new imperative-sentence fallback cases.
>
> **Tradeoffs:** The imperative verb list is a fixed heuristic — a production system would use an LLM for this, but the heuristic is sufficient for the assignment.

c. Graphite Diamond generated code review
> TODO (Graphite AI review)

## Task 3: Try adding a new model and relationships
a. Links to relevant commits/issues
> TODO (not completed)

b. PR Description
> Not completed. This task required adding a new database model (e.g., Tag or Category) with a foreign key relationship to Note. The models.py currently only has Note and ActionItem as independent models.

c. Graphite Diamond generated code review
> Not applicable — task not completed.

## Task 4: Improve tests for pagination and sorting
a. Links to relevant commits/issues
> TODO (PR link)

b. PR Description
> **Problem:** The starter test suite had minimal coverage — no tests for pagination parameters, sort order, or filter queries.
>
> **Approach:** Added comprehensive tests to `backend/tests/test_db.py` (240 lines) covering:
> - Creating multiple notes and verifying `skip`/`limit` pagination
> - Verifying `sort_by=created_at` with `order=asc`/`desc`
> - `note_id` filtering for action items
> - Edge cases: empty database, single item, large skip value
>
> All 23 tests pass: `23 passed, 25 warnings in 1.11s`.
>
> **Tradeoffs:** Tests use an in-memory SQLite database via pytest fixtures — this covers the ORM layer but not potential differences in production database behavior.

c. Graphite Diamond generated code review
> TODO (Graphite AI review)

## Brief Reflection
a. The types of comments you typically made in your manual reviews (e.g., correctness, performance, security, naming, test gaps, API shape, UX, docs).
> In manual reviews, comments focused primarily on:
> - **Correctness:** Checking that 404 handlers were present for all GET-by-ID endpoints; verifying that pagination `skip` and `limit` had sensible defaults and validation (e.g., limit ≤ 100)
> - **Test gaps:** Noting missing edge cases (empty input, sort order reversal, items with same timestamp)
> - **API shape:** Checking that response models matched what was actually returned (e.g., `orm_mode = True` set correctly)
> - **Naming:** Flagging inconsistent naming between `note_id` filter parameter and the model field name

b. A comparison of **your** comments vs. **Graphite’s** AI-generated comments for each PR.
> TODO (Graphite AI review results needed to complete this comparison)

c. When the AI reviews were better/worse than yours (cite specific examples)
> TODO (requires Graphite Diamond PR reviews to compare)

d. Your comfort level trusting AI reviews going forward and any heuristics for when to rely on them.
> Based on experience with Claude Code during this assignment: AI reviews are reliable for catching missing error handling, incomplete validation, and obvious naming inconsistencies. They are less reliable for domain-specific correctness (e.g., "does this business logic make sense?") and for catching test gaps that require understanding the intended behavior rather than just the code structure. My heuristic going forward: trust AI reviews for mechanical/structural feedback (imports, error codes, schema consistency), but always do a manual pass for semantic correctness and test coverage gaps. 



