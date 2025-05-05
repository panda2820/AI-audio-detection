from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse, FileResponse
import tempfile
import os
from models import AudioAnalysisResponse
from services.transcription import transcribe_audio
from services.detection import detect_ai_audio
from typing import List

app = FastAPI()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "upload")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze-audio", response_model=AudioAnalysisResponse)
def analyze_audio(file: UploadFile = File(...)):
    if file.content_type not in ["audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only WAV and MP3 are supported.")
    upload_dir = os.path.join(os.path.dirname(__file__), "upload")
    os.makedirs(upload_dir, exist_ok=True)
    unique_filename = file.filename
    file_path = os.path.join(upload_dir, unique_filename)
    try:
        file.file.seek(0)
        with open(file_path, "wb") as out_file:
            out_file.write(file.file.read())
        is_ai, description = detect_ai_audio(file_path)
        transcription = transcribe_audio(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
    return AudioAnalysisResponse(
        is_ai_audio=is_ai,
        description=description,
        transcription=transcription
    )

@app.get("/upload")
def upload_page():
    html_path = os.path.join(os.path.dirname(__file__), "views", "upload.html")
    return FileResponse(html_path, media_type="text/html")

@app.post("/upload-file")
def upload_file(file: UploadFile = File(...), filename: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    file.file.seek(0)
    with open(file_path, "wb") as out_file:
        out_file.write(file.file.read())
    return {"message": f"File '{filename}' uploaded successfully."}

@app.get("/list-uploaded-files", response_model=List[str])
def list_uploaded_files():
    return [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]

@app.post("/analyze-uploaded-file", response_model=AudioAnalysisResponse)
def analyze_uploaded_file(filename: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    is_ai, description = detect_ai_audio(file_path)
    transcription = transcribe_audio(file_path)
    return AudioAnalysisResponse(
        is_ai_audio=is_ai,
        description=description,
        transcription=transcription
    ) 