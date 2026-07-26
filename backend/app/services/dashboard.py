from sqlalchemy.orm import Session

from app.models.official import OFFICIAL_TABLES
from app.repositories.official import OfficialTableRepository
from app.schemas.analytics import DashboardSummary


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def summary(self) -> DashboardSummary:
        totals = {}
        for table in ("CaseMaster", "Victim", "Accused", "District", "Unit"):
            if table in OFFICIAL_TABLES:
                totals[table] = OfficialTableRepository(self.db, table).count()
        return DashboardSummary(totals=totals, recent_activity=[])

