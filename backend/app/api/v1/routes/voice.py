from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import require_permission
from app.schemas.auth import CurrentUser
from app.schemas.voice import VoiceTranscriptRequest, VoiceTranscriptResponse
from app.services.voice import VoiceService

router = APIRouter()


@router.post("/transcribe", response_model=VoiceTranscriptResponse)
def transcribe(
    payload: VoiceTranscriptRequest,
    user: Annotated[CurrentUser, Depends(require_permission("voice:use"))],
) -> VoiceTranscriptResponse:
    return VoiceService().transcribe(payload)

