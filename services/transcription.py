import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

WHISPER_API_URL = "https://api.groq.com/openai/v1/audio/transcriptions"


def transcribe_audio(file_path: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set in environment.")
    with open(file_path, "rb") as audio_file:
        files = {"file": audio_file}
        data = {"model": "whisper-large-v3"}
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
        response = requests.post(WHISPER_API_URL, files=files, data=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("text", "") 