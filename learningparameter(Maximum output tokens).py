
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = "Explain Artificial Intelligence in detail."

token_limits = [30, 75, 150]

for limit in token_limits:

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=limit,
        temperature=0.3
    )

    print("\nMAX OUTPUT TOKENS:", limit)
    print("RESPONSE:")
    print(response.choices[0].message.content)

    print(
        "FINISH REASON:",
        response.choices[0].finish_reason
    )
