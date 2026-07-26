from pydantic import BaseModel


class VoiceTranscriptRequest(BaseModel):
    audio_base64: str
    language: str = "en-IN"


class VoiceTranscriptResponse(BaseModel):
    transcript: str
    confidence_score: float

