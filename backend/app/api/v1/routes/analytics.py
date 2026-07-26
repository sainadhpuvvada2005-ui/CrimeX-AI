from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.deps import DbSession, require_permission
from app.schemas.analytics import AnalyticsRequest, AnalyticsResponse
from app.schemas.auth import CurrentUser
from app.services.analytics import AnalyticsService

router = APIRouter()


@router.post("/cases/aggregate", response_model=AnalyticsResponse)
def aggregate_cases(
    payload: AnalyticsRequest,
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("analytics:read"))],
) -> AnalyticsResponse:
    return AnalyticsService(db).aggregate_cases(payload.dimension, payload.filters)

