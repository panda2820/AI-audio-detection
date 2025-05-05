from pydantic import BaseModel
from typing import Optional

class AudioAnalysisResponse(BaseModel):
    is_ai_audio: bool
    description: str
    transcription: Optional[str] = None 