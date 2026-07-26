from typing import Any

from sqlalchemy.orm import Session

from app.repositories.official import OfficialTableRepository
from app.schemas.analytics import AnalyticsResponse


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def aggregate_cases(self, dimension: str, filters: dict[str, Any]) -> AnalyticsResponse:
        repo = OfficialTableRepository(self.db, "CaseMaster")
        rows = repo.aggregate(dimension=dimension, filters=filters)
        return AnalyticsResponse(dimension=dimension, items=rows)

