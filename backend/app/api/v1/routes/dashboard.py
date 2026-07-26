from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession, require_permission
from app.schemas.analytics import DashboardSummary
from app.schemas.auth import CurrentUser
from app.services.dashboard import DashboardService

router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def summary(
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("dashboard:read"))],
) -> DashboardSummary:
    return DashboardService(db).summary()

