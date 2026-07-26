from typing import Any

from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str


class SearchParams(BaseModel):
    q: str | None = Field(default=None, description="Free text search term")
    filters: dict[str, Any] = Field(default_factory=dict, description="Field filters applied by service allowlist")


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    metadata: dict[str, Any] = Field(default_factory=dict)

