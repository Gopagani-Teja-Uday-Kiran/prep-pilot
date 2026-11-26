import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR/'.venv/.env')
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL=os.getenv("GEMINI_MODEL","gemini-2.5-flash")
GROQ_MODEL=os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")
def validate_config():
    missing=[]
    if not GEMINI_MODEL:
        missing.append("GEMINI_MODEL")
    if not GROQ_MODEL:
        missing.append("GROQ_MODEL")
    if missing:
        raise ValueError("Missing required environment variables:" + ",".join(missing))
