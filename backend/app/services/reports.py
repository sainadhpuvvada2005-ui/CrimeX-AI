import uuid

from sqlalchemy.orm import Session

from app.schemas.report import ReportRequest, ReportResponse


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ReportRequest) -> ReportResponse:
        report_id = str(uuid.uuid4())
        return ReportResponse(
            report_id=report_id,
            status="queued",
            download_url=None,
            metadata={"report_type": payload.report_type, "filters": payload.filters},
        )

