
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from your environment or .env file")

client = Groq(api_key=api_key)

prompt = """
Write a creative opening sentence
for a robo and lion story.
"""

temperatures = [0.0, 0.3, 0.7, 1.0, 1.5]
#0.0	More predictable
#0.2	Relatively consistent
#0.5	Balanced
#0.8	More varied
#1.0	More exploratory
#1.5	Highly varied
#2.0	Very high variation, if supported
for temperature in temperatures:

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_completion_tokens=100
    )

    print("\nTEMPERATURE:", temperature)
    print("RESPONSE:", response.choices[0].message.content)
