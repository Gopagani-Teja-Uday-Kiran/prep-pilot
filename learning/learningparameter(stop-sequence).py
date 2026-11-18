
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages=[
        {
            "role": "user",
            "content": """
            Count from 1 to 10.with spellings
            Put each number on a new line.
            """
        }
    ],
    stop=["7"],
    max_completion_tokens=100
)

print("GENERATED RESPONSE:")
print(response.choices[0].message.content)

print("\nFINISH REASON:")
print(response.choices[0].finish_reason)
