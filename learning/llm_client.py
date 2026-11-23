
import os
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError("GROQ_API_KEY is missing from the .env file beside this script.")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"


def generate_response(prompt, temperature=0.7):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("Groq returned no text.")
    return content
