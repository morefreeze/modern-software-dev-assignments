# Week 2 Write-up
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
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt:
```
Add an LLM-based action item extraction function `extract_action_items_llm(text: str) -> List[str]`
to `app/services/extract.py`. Use Ollama with the llama3 model via `ollama.chat()`. The function
should call the LLM with a system prompt instructing it to extract action items one per line,
then parse the response line by line, filtering out empty lines and meta-commentary. Handle
errors with a try/except that returns an empty list.
```

Generated Code Snippets:
```
app/services/extract.py  lines 69-105  (extract_action_items_llm function)
```

### Exercise 2: Add Unit Tests
Prompt:
```
Add pytest unit tests for `extract_action_items_llm` to `tests/test_extract.py`. Include tests for:
1. Basic extraction from text with bullet-point action items (assert expected keywords appear in output)
2. Empty string input (assert returns [])
3. Text with no action items (assert returns [])
4. Keyword-prefixed lines (Todo:/Action:/Next: prefixes, assert expected keywords appear)
Keep the existing test_extract_bullets_and_checkboxes test. Use the actual Ollama integration
(no mocks) since the function is designed for real LLM calls.
```

Generated Code Snippets:
```
tests/test_extract.py  lines 22-66  (4 new test functions added)
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt:
```
Refactor the app to use Pydantic schemas for all request/response models. Create
`app/schemas/__init__.py` with the following models: NoteCreate, Note (with orm_mode=True),
ActionItem (with orm_mode=True), ExtractActionItemsRequest (with save_note bool field),
ActionItemCreate, and ExtractActionItemsResponse. Add field descriptions and docstrings.
Update the routers to import and use these schemas as response_model parameters and type
annotations. Add docstrings to all router functions.
```

Generated/Modified Code Snippets:
```
app/schemas/__init__.py  lines 1-52   (entire new file: NoteCreate, Note, ActionItem,
                                       ExtractActionItemsRequest, ActionItemCreate,
                                       ExtractActionItemsResponse)
app/routers/action_items.py  lines 1-14  (updated imports to use schemas)
app/routers/action_items.py  lines 18-19  (added response_model=ExtractActionItemsResponse)
app/routers/action_items.py  lines 40-42  (added /extract-llm response_model)
app/routers/notes.py  lines 1-10  (updated imports)
app/routers/notes.py  (added response_model annotations and docstrings throughout)
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt:
```
Using agentic mode, make the following changes as a single coordinated task:
1. Add a POST /action-items/extract-llm endpoint to app/routers/action_items.py that calls
   extract_action_items_llm() and returns an ExtractActionItemsResponse.
2. Add a GET /notes endpoint to app/routers/notes.py that returns a list of all notes.
3. In frontend/index.html, add an "Extract LLM" button next to the existing Extract button,
   and a "List Notes" button. Wire both buttons with JavaScript fetch calls to the new endpoints.
   Display results in the existing output area.
```

Generated Code Snippets:
```
app/routers/action_items.py  lines 37-55  (POST /extract-llm endpoint)
app/routers/notes.py  lines 31-38        (GET /notes list endpoint)
frontend/index.html                       (Extract LLM button + List Notes button + JS handlers)
```


### Exercise 5: Generate a README from the Codebase
Prompt:
```
Generate a README.md for the week2 Action Item Extractor project. Include:
- Project overview and features (heuristic extraction + LLM extraction via Ollama)
- Requirements (Python 3.10+, Ollama with llama3, Poetry)
- Setup instructions (poetry install, ollama pull llama3)
- How to run the app (uvicorn command)
- API endpoint reference table for /notes and /action-items
- Example request body for extraction endpoints
- How to run tests (pytest command, note about Ollama requirement)
- Project structure tree with brief description of each file
```

Generated Code Snippets:
```
README.md  (entire file, generated from codebase inspection)
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 