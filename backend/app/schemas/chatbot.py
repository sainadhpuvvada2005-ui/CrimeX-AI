from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    language: str = Field(default="en", pattern="^(en|kn)$")
    enable_voice_output: bool = False
    execute_sql: bool = True


class ChatResponse(BaseModel):
    session_id: str | None = None
    answer: str
    intent: str
    language: str = "en"
    generated_sql: str | None = None
    sql_rows: list[dict[str, Any]] = Field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = Field(default_factory=list)
    explanation: dict[str, Any] = Field(default_factory=dict)
    confidence_score: float
    voice_text: str | None = None


class ChatMemoryItem(BaseModel):
    message_sequence: int
    user_prompt: str
    assistant_response: str | None = None
    intent_name: str | None = None
    generated_sql: str | None = None


class ChatMemoryResponse(BaseModel):
    session_id: str
    items: list[ChatMemoryItem]


class PdfExportRequest(BaseModel):
    session_id: str | None = None
    title: str = "CrimeX AI Conversation Report"
    messages: list[dict[str, Any]] = Field(default_factory=list)
