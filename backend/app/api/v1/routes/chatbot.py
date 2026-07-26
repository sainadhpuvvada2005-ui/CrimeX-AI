from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.api.deps import DbSession, require_permission
from app.schemas.auth import CurrentUser
from app.schemas.chatbot import ChatMemoryResponse, ChatRequest, ChatResponse, PdfExportRequest
from app.services.chatbot import ChatbotService

router = APIRouter()


@router.post("/ask", response_model=ChatResponse)
def ask(
    payload: ChatRequest,
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("chatbot:use"))],
) -> ChatResponse:
    return ChatbotService(db).ask(payload, user)


@router.get("/memory/{session_id}", response_model=ChatMemoryResponse)
def memory(
    session_id: str,
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("chatbot:use"))],
) -> ChatMemoryResponse:
    return ChatbotService(db).memory(session_id)


@router.post("/export/pdf")
def export_pdf(
    payload: PdfExportRequest,
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("chatbot:use"))],
) -> Response:
    content = ChatbotService(db).export_pdf(payload)
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="crimex-chatbot-report.pdf"'},
    )
