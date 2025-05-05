# FastAPI Audio Analysis Backend

## Features
- Upload `.wav` or `.mp3` audio files for analysis
- Transcribes audio using Whisper via Groq API
- Detects if audio is AI-generated (stub logic, replaceable)
- Returns a JSON report with results and reasoning

## Setup
1. Clone the repo and navigate to the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the `backend` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

## Running the Server
```bash
uvicorn main:app --reload
```

## API Usage
- **POST** `/analyze-audio`
  - Form-data: `file` (audio/wav or audio/mp3)
  - Response: JSON with `is_ai_audio`, `description`, and `transcription`

## Notes
- The AI audio detection is a stub. Replace the logic in `services/detection.py` for real detection.
- No database is used; all analysis is one-time and in-memory. 