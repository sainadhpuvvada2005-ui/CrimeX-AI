from typing import Any

from sqlalchemy.orm import Session

from app.repositories.official import OfficialTableRepository
from app.schemas.case import CaseDetailResponse
from app.utils.pagination import Page, PageParams


class CaseService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OfficialTableRepository(db, "CaseMaster")

    def search(self, page: PageParams, q: str | None, filters: dict[str, Any]) -> Page[dict[str, Any]]:
        items, total = self.repo.list(page, search=q, filters=filters)
        return Page(items=items, total=total, page=page.page, size=page.size)

    def detail(self, case_id: str) -> CaseDetailResponse:
        case = self.repo.get_by_primary_key(case_id)
        if not case:
            return CaseDetailResponse(case={}, related={})
        return CaseDetailResponse(case=case, related={})


class OfficialEntityService:
    def __init__(self, db: Session, table_name: str):
        self.repo = OfficialTableRepository(db, table_name)

    def search(self, page: PageParams, q: str | None, filters: dict[str, Any]) -> Page[dict[str, Any]]:
        items, total = self.repo.list(page, search=q, filters=filters)
        return Page(items=items, total=total, page=page.page, size=page.size)

