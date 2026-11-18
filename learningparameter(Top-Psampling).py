"""
It controls the selection of tokens by considering the smallest group of candidate tokens whose cumulative probability reaches a specified threshold.
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = """
Write a short creative story about
a robot discovering a hidden forest.
"""

top_p_values = [0.3, 0.6, 0.9, 1.0]

for value in top_p_values:

    response = client.chat.completions.create(
        # llama-3.3-70b-versatile was deprecated for developer-tier access.
        model="qwen/qwen3.8-27b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        top_p=value,
        max_completion_tokens=150
    )

    print("\nTOP-P:", value)
    print(response.choices[0].message.content)
