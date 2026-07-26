from typing import Any

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    prediction_type: str = "crime-risk"
    filters: dict[str, Any] = Field(default_factory=dict)


class PredictionResponse(BaseModel):
    prediction_id: str | None = None
    prediction_type: str
    result: dict[str, Any]
    confidence_score: float
    explanation: dict[str, Any]

