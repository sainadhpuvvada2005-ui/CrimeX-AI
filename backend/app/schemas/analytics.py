from typing import Any

from pydantic import BaseModel, Field


class DashboardSummary(BaseModel):
    totals: dict[str, Any]
    recent_activity: list[dict[str, Any]] = Field(default_factory=list)


class AnalyticsRequest(BaseModel):
    dimension: str = "CrimeHead"
    filters: dict[str, Any] = Field(default_factory=dict)


class AnalyticsResponse(BaseModel):
    dimension: str
    items: list[dict[str, Any]]

