from typing import Any

from pydantic import BaseModel, Field


class ReportRequest(BaseModel):
    report_type: str
    filters: dict[str, Any] = Field(default_factory=dict)
    include_sections: list[str] = Field(default_factory=list)


class ReportResponse(BaseModel):
    report_id: str
    status: str
    download_url: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)

