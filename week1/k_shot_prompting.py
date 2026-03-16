import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = """Your task: reverse the order of the letters in the given word.

How to reverse: write the word backwards. Start from the last character and go to the first.

Example 1:
Original: h e l l o → Reverse: o l l e h → Output: olleh

Example 2:
Original: p y t h o n → Reverse: n o h t y p → Output: nohtyp

Example 3:
Original: c o d i n g → Reverse: g n i d o c → Output: gnidoc

What you need to do:
1. Take the input word "httpstatus"
2. Write its letters: h t t p s t a t u s
3. Write it backwards starting from the last character
4. Output ONLY the reversed word, nothing else

Output only the reversed word: no explanations, no extra text."""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)