from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession, require_permission
from app.schemas.auth import CurrentUser
from app.schemas.report import ReportRequest, ReportResponse
from app.services.reports import ReportService

router = APIRouter()


@router.post("/pdf", response_model=ReportResponse)
def create_pdf_report(
    payload: ReportRequest,
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("report:create"))],
) -> ReportResponse:
    return ReportService(db).create(payload)

