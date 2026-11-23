
from llm_client import generate_response

question = input("Enter a question: ")

answers = []

for i in range(5):
    prompt = f"""
    Answer this educational question.

    Question: {question}

    Provide:
    - Final answer
    - Brief explanation

    Be accurate and concise.
    """

    answer = generate_response(
        prompt,
        temperature=0.7
    )

    answers.append(answer)

    print(f"\nAttempt {i+1}")
    print(answer)


summary_prompt = f"""
Compare the following five answers:

{answers}

Identify:
1. Their common conclusions.
2. Differences.
3. Possible errors.
4. The most defensible answer.

Do not assume the majority answer is automatically correct.
"""

print("\nCOMPARISON\n")
print(generate_response(summary_prompt))
