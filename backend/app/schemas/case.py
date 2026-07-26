from typing import Any

from pydantic import BaseModel, Field


class CaseSearchRequest(BaseModel):
    q: str | None = None
    filters: dict[str, Any] = Field(default_factory=dict)


class OfficialRecord(BaseModel):
    data: dict[str, Any]


class CaseDetailResponse(BaseModel):
    case: dict[str, Any]
    related: dict[str, list[dict[str, Any]]] = Field(default_factory=dict)

