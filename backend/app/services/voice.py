from app.schemas.voice import VoiceTranscriptRequest, VoiceTranscriptResponse


class VoiceService:
    def transcribe(self, payload: VoiceTranscriptRequest) -> VoiceTranscriptResponse:
        return VoiceTranscriptResponse(
            transcript="Voice provider is not configured. Submit text query through chatbot.",
            confidence_score=0.0,
        )

