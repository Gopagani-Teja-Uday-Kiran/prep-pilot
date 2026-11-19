import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"))

from google import genai
from google.genai import errors

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is missing from the .env file beside this script.")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents="explain about AI",
    )
except errors.ServerError:
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="explain about AI",
    )

print("Response:", repr(response.text))
