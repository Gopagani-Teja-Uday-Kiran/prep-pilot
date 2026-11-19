from groq import Groq
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from the .env file beside this script.")

client = Groq(api_key=api_key)
response=client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "user", "content": "explain about AI"}
    ]
)
print("Response:", repr(response.choices[0].message.content))
