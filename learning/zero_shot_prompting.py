
from llm_client import generate_response

subject = input("Enter subject: ")
topic = input("Enter topic: ")

count = int(input("Number of questions: "))

prompt = f"""
You are an educational quiz generator.

Generate {count} multiple-choice questions.

Subject: {subject}
Topic: {topic}

Requirements:
- Four options per question.
- Only one correct answer.
- Provide the correct answer.
- Explain why it is correct.
- Use beginner-friendly language.

Do not include sample questions.
"""

result = generate_response(prompt)

print("\nGENERATED QUIZ\n")
print(result)
