# Week 1 - Prompting Techniques Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete all 6 prompting technique exercises by designing effective prompts that pass the test cases in each file.

**Architecture:** Each file implements a different prompting technique with a pre-defined scaffold. We only need to fill in the TODO sections (system prompts, context selection, reflexion prompts) and iterate until tests pass.

**Tech Stack:** Python, Ollama (llama3.1:8b, mistral-nemo:12b)

---

## Overview of Files to Modify

| File | Technique | What Needs to Change |
|------|-----------|----------------------|
| `week1/k_shot_prompting.py` | K-shot prompting | Fill `YOUR_SYSTEM_PROMPT` |
| `week1/chain_of_thought.py` | Chain-of-thought | Fill `YOUR_SYSTEM_PROMPT` |
| `week1/tool_calling.py` | Tool calling | Fill `YOUR_SYSTEM_PROMPT` |
| `week1/self_consistency_prompting.py` | Self-consistency prompting | Fill `YOUR_SYSTEM_PROMPT` |
| `week1/rag.py` | RAG (Retrieval-Augmented Generation) | Fill `YOUR_SYSTEM_PROMPT` and `YOUR_CONTEXT_PROVIDER` |
| `week1/reflexion.py` | Reflexion | Fill `YOUR_REFLEXION_PROMPT` and implement `your_build_reflexion_context` |

---

### Task 1: K-shot Prompting

**Files:**
- Modify: `week1/k_shot_prompting.py:10-12`

**Task Description:**
The task is to reverse the letters in the word "httpstatus". Expected output is "sutatsptth".
K-shot prompting means we provide examples in the prompt to help the model understand what to do.

- [ ] **Step 1: Fill in YOUR_SYSTEM_PROMPT with k-shot examples**

```python
YOUR_SYSTEM_PROMPT = """You are a word reversal assistant. Follow the examples carefully.

Examples:
Input: hello → Output: olleh
Input: world → Output: dlrow
Input: python → Output: nohtyp
Input: prompting → Output: gnitemorp

Now, reverse the given word according to this pattern. Only output the reversed word, nothing else."""
```

- [ ] **Step 2: Run the test**

Run: `cd week1 && python k_shot_prompting.py`
Expected: "SUCCESS" when it outputs "sutatsptth"

- [ ] **Step 3: Commit**

```bash
git add week1/k_shot_prompting.py
git commit -m "week1: complete k_shot_prompting"
```

---

### Task 2: Chain-of-Thought Prompting

**Files:**
- Modify: `week1/chain_of_thought.py:11-12`

**Task Description:**
Solve the word problem: "Henry made two stops during his 60-mile bike trip. He first stopped after 20 miles. His second stop was 15 miles before the end of the trip. How many miles did he travel between his first and second stops?"
Expected answer: 25. Chain-of-thought encourages the model to work through step-by-step.

- [ ] **Step 1: Fill in YOUR_SYSTEM_PROMPT with chain-of-thought instruction**

```python
YOUR_SYSTEM_PROMPT = """Solve this problem step-by-step. First, understand what is given, then work through each calculation step carefully. Show your reasoning before giving the final answer. Think through each step explicitly to avoid mistakes."""
```

- [ ] **Step 2: Run the test (5 runs with majority voting)**

Run: `cd week1 && python chain_of_thought.py`
Expected: Majority answer should be "Answer: 25" → "SUCCESS"

- [ ] **Step 3: Commit if passes**

```bash
git add week1/chain_of_thought.py
git commit -m "week1: complete chain_of_thought"
```

---

### Task 3: Tool Calling

**Files:**
- Modify: `week1/tool_calling.py:72-73`

**Task Description:**
The model needs to call the `output_every_func_return_type` tool with the correct JSON format to analyze this file's function return types.

- [ ] **Step 1: Fill in YOUR_SYSTEM_PROMPT with tool calling instructions**

```python
YOUR_SYSTEM_PROMPT = """You have access to the following tool:

Tool: output_every_func_return_type
Description: Return a newline-delimited list of "name: return_type" for each top-level function in a file.
Arguments: file_path (string, optional) - the path to the file to analyze. Defaults to the current file if not provided.

You must respond with ONLY a valid JSON object in the format:
{{"tool": "output_every_func_return_type", "args": {{"file_path": "{file_path}"}}}}

Call the tool now to list all function return types in this file. No extra text, just the JSON."""
```

- [ ] **Step 2: Run the test**

Run: `cd week1 && python tool_calling.py`
Expected: Valid tool call that produces correct output → "SUCCESS"

- [ ] **Step 3: Commit if passes**

```bash
git add week1/tool_calling.py
git commit -m "week1: complete tool_calling"
```

---

### Task 4: Self-Consistency Prompting

**Files:**
- Modify: `week1/self_consistency_prompting.py:10-11`

**Task Description:**
Calculate 3^12345 mod 100. Expected answer is 43. Self-consistency involves prompting the model to reason carefully and then taking the majority answer across multiple runs.

- [ ] **Step 1: Fill in YOUR_SYSTEM_PROMPT with instructions for careful reasoning**

```python
YOUR_SYSTEM_PROMPT = """Calculate this modular exponentiation problem step-by-step. Use Euler's theorem or pattern spotting to simplify. Show all your work clearly before giving the final answer. Check your calculation carefully to avoid arithmetic errors."""
```

- [ ] **Step 2: Run the test (up to 5 runs)**

Run: `cd week1 && python self_consistency_prompting.py`
Expected: At least one run produces "Answer: 43" → "SUCCESS"

- [ ] **Step 3: Commit if passes**

```bash
git add week1/self_consistency_prompting.py
git commit -m "week1: complete self_consistency_prompting"
```

---

### Task 5: RAG (Retrieval-Augmented Generation)

**Files:**
- Modify: `week1/rag.py:39-40` and `week1/rag.py:54-59`

**Task Description:**
Write a Python function `fetch_user_name(user_id: str, api_key: str) -> str` using the provided API documentation. Need to:
1. Select the relevant context from the corpus (the API docs)
2. Write an effective system prompt

- [ ] **Step 1: Update YOUR_CONTEXT_PROVIDER to return the API docs**

```python
def YOUR_CONTEXT_PROVIDER(corpus: List[str]) -> List[str]:
    """Select and return the relevant subset of documents from CORPUS for this task.
    """
    return [corpus[0]]  # Return the API docs from data/api_docs.txt
```

- [ ] **Step 2: Fill in YOUR_SYSTEM_PROMPT**

```python
YOUR_SYSTEM_PROMPT = """You are a Python coding assistant. Use only the provided context documentation to write the correct function. Follow the API documentation exactly for the base URL, endpoint, authentication header, and error handling. Output only the Python code in a single code block."""
```

- [ ] **Step 3: Run the test**

Run: `cd week1 && python rag.py`
Expected: Output contains all required snippets → "SUCCESS"

- [ ] **Step 4: Commit if passes**

```bash
git add week1/rag.py
git commit -m "week1: complete rag"
```

---

### Task 6: Reflexion

**Files:**
- Modify: `week1/reflexion.py:17-18` and `week1/reflexion.py:94-99`

**Task Description:**
Implement the reflexion technique: given an initial incorrect implementation and test failures, reflect on the mistakes and produce a corrected version. Need to:
1. Implement `your_build_reflexion_context` to create the reflection prompt context
2. Fill in `YOUR_REFLEXION_PROMPT` (system prompt for reflexion)

Password validation rules:
- At least 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character from `!@#$%^&*()-_`
- No whitespace

- [ ] **Step 1: Implement your_build_reflexion_context**

```python
def your_build_reflexion_context(prev_code: str, failures: List[str]) -> str:
    """Build the user message for the reflexion step using prev_code and failures.
    """
    return f"""Your previous implementation was:
```python
{prev_code}
```

It failed the following tests:
{chr(10).join('- ' + f for f in failures)}

Analyze what went wrong, then fix the implementation. Provide the corrected full code in a Python code block."""
```

- [ ] **Step 2: Fill in YOUR_REFLEXION_PROMPT (system prompt)**

```python
YOUR_REFLEXION_PROMPT = """You are a code reviewer and debugging assistant. Given the previous incorrect implementation and the failing test cases, identify the bug(s) and provide the corrected implementation of is_valid_password(password: str) -> bool that will pass all the tests. Output ONLY a single fenced Python code block with the corrected function."""
```

- [ ] **Step 3: Run the test**

Run: `cd week1 && python reflexion.py`
Expected: After reflexion, the implementation passes all tests → "SUCCESS"

- [ ] **Step 4: Commit if passes**

```bash
git add week1/reflexion.py
git commit -m "week1: complete reflexion"
```

---

### Task 7: Create plan.md with key learnings

**Files:**
- Create: `week1/plan.md`

- [ ] **Step 1: Document key points and learnings for each technique**

Include:
- What prompt you used
- Why you chose it
- Any iterations you needed
- Key insights

- [ ] **Step 2: Mark all tasks as complete with [x]**

- [ ] **Step 3: Commit**

```bash
git add week1/plan.md
git commit -m "week1: add plan.md with learnings"
```

---

### Task 8: Final verification

- [ ] **Step 1: Run all tests to verify everything passes**

```bash
cd week1
python k_shot_prompting.py
python chain_of_thought.py
python tool_calling.py
python self_consistency_prompting.py
python rag.py
python reflexion.py
```

- [ ] **Step 2: Check git status, verify all changes are committed**

```bash
git status
```

---

Plan complete. Ready to execute.
