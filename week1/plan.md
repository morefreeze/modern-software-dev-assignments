# Week 1 - Prompting Techniques: Key Learnings

This document records the key points and learnings from completing each prompting technique.

## [x] 1. K-shot Prompting

**File:** `week1/k_shot_prompting.py`

**Task:** Reverse the word "httpstatus" → expected output "sutatsptth"

**Prompt Design:**
- First attempt: General examples with 4 examples → model got it wrong, kept grouping letters incorrectly
- Second attempt: Spelled out the letters explicitly to show the reversal process → still wrong on first try but passed on second try
- Final prompt: Clear instruction on how reversal works (first ↔ last, etc.) with multiple examples showing the process

**Key Insights:**
- K-shot prompting works best when the examples are clear and directly relevant to the task
- For simple pattern tasks like string reversal, spelling out the process explicitly helps the model understand better
- Sometimes you need multiple runs (temperature > 0) to get the correct output

**Final Result:** ✅ Passed (success on second run)

---

## [x] 2. Chain-of-Thought Prompting

**File:** `week1/chain_of_thought.py`

**Task:** Calculate 3^12345 (mod 100) → expected answer 43

**Prompt Design:**
- Instructed the model to find the repeating pattern (cycle)
- Guide it to use cycle detection to reduce the exponent
- Emphasize checking the pattern and arithmetic twice

**Key Insights:**
- Chain-of-thought prompting encourages step-by-step reasoning which reduces arithmetic errors
- For mathematical problems, explicitly mentioning the method (cyclicity/Euler's theorem) helps the model use the right approach
- The llama3.1:8b model found the correct cycle (cycle length 20) and calculated 12345 mod 20 = 5 → 3^5 = 243 → 243 mod 100 = 43 correctly

**Final Result:** ✅ Passed (success on first run)

---

## [x] 3. Tool Calling

**File:** `week1/tool_calling.py`

**Task:** Model must output valid JSON to call `output_every_func_return_type` on the current file

**Prompt Design:**
- Clear description of the tool
- Explicit JSON format requirement
- Example provided
- Emphasized no extra text, only JSON

**Key Insights:**
- Tool calling requires very clear formatting instructions
- Models can struggle with JSON output if not explicitly instructed about the exact format
- Providing an example of the expected JSON greatly improves success rate

**Final Result:** ✅ Passed (success on first try)

**Interesting Note:** The model output `{"tool": "output_every_func_return_type", "args": {}}` which was fine because the code defaults to the current file. The output matched perfectly.

---

## [x] 4. Self-Consistency Prompting

**File:** `week1/self_consistency_prompting.py`

**Task:** Henry's bike trip problem → expected answer 25 miles between stops

**Prompt Design:**
- Step-by-step reasoning guidance
- Emphasize double-checking arithmetic
- Self-consistency relies on majority voting across multiple runs

**Key Insights:**
- Self-consistency helps when the problem can have multiple reasoning paths but one is correct more often than not
- Even with temperature=1 (high variation), majority voting still landed on the correct answer (2/5 runs were correct, majority)
- The prompt needs to encourage careful step-by-step reasoning for self-consistency to work well

**Final Result:** ✅ Passed (majority answer was correct: Answer: 25)

---

## [x] 5. RAG (Retrieval-Augmented Generation)

**File:** `week1/rag.py`

**Task:** Write `fetch_user_name()` function based on provided API documentation

**Prompt Design:**
- Instruct model to use only the provided context
- Emphasize following the docs exactly for URL, auth, error handling
- The `YOUR_CONTEXT_PROVIDER` returns the full API doc from `data/api_docs.txt`

**Key Insights:**
- RAG grounds the model's output in the provided documentation
- By selecting the right context (the full API doc), the model got everything right: correct base URL, endpoint path, X-API-Key header, requests.get, error handling with `raise_for_status()`, returning the name field
- The required snippets were all present in the first generated output

**Final Result:** ✅ Passed (success on first run)

---

## [x] 6. Reflexion

**File:** `week1/reflexion.py`

**Task:** Implement password validation with reflexion - start with incorrect code, then improve based on failing tests

**Implementation:**
- `YOUR_REFLEXION_PROMPT`: System prompt that explains the task, lists the exact rules, asks for corrected code
- `your_build_reflexion_context`: Includes the previous code and the list of failing tests, asks model to identify bugs and fix

**Key Insights:**
- Reflexion is a powerful technique that uses the model's own ability to debug and improve its output
- The initial implementation was incomplete (just checked length, any alpha, any digit - missed separate uppercase/lowercase check and special character check)
- After being given the failing tests, the model correctly identified all the missing checks and fixed the implementation
- Reflexion is particularly useful for code generation where you can automatically test and get failure feedback

**Final Result:** ✅ Passed (one iteration was enough to fix all failing tests)

---

## Summary

| Technique | Files Modified | Result |
|-----------|----------------|--------|
| K-shot Prompting | `k_shot_prompting.py` | ✅ Passed |
| Chain-of-Thought | `chain_of_thought.py` | ✅ Passed |
| Tool Calling | `tool_calling.py` | ✅ Passed |
| Self-Consistency | `self_consistency_prompting.py` | ✅ Passed |
| RAG | `rag.py` | ✅ Passed |
| Reflexion | `reflexion.py` | ✅ Passed |

## Key Takeaways

1. **Different techniques are useful for different problems:**
   - K-shot: Good for teaching the model a specific output pattern
   - CoT: Improves reasoning on math/logic problems
   - Tool calling: Enables LLMs to interact with external tools/code
   - Self-consistency: Improves accuracy through majority voting on multiple reasoning paths
   - RAG: Grounds generation in external knowledge/documentation
   - Reflexion: Uses iterative feedback to improve output starting from an initial attempt

2. **Prompt engineering matters:** Clear instructions + examples + format specification greatly improve model output.

3. **All 6 techniques work as expected with llama3.1:8b and mistral-nemo:12b when the prompt is clear.
