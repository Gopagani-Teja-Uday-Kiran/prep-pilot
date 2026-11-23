
from llm_client import generate_response

original_prompt = input("Enter your original prompt: ")

meta_prompt = f"""
You are an expert prompt engineer.

Analyze the following prompt:

{original_prompt}

Identify:
1. Ambiguous instructions.
2. Missing requirements.
3. Unclear output format.
4. Possible improvements.

Then generate an improved version.

Return:
- Original prompt problems
- Improved prompt
- Explanation of improvements
"""

result = generate_response(meta_prompt)

print("\nIMPROVED PROMPT\n")
print(result)
