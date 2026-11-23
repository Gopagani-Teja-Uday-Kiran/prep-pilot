
from llm_client import generate_response

chapter = input("Enter chapter content: ")

summary_prompt = f"""
Summarize the following educational chapter.

Include:
- Important concepts
- Definitions
- Key points

Chapter:
{chapter}
"""

summary = generate_response(summary_prompt)

quiz_prompt = f"""
Generate 5 MCQs using the following summary.

Summary:
{summary}

Include four options, correct answer,
and explanation for each question.
"""

quiz = generate_response(quiz_prompt)

revision_prompt = f"""
Create short revision notes using:

{summary}

Keep the notes suitable for exam preparation.
"""

notes = generate_response(revision_prompt)

print("\nSUMMARY\n", summary)
print("\nQUIZ\n", quiz)
print("\nREVISION NOTES\n", notes)
