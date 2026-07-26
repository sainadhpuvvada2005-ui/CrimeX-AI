from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.deps import DbSession, require_permission
from app.schemas.auth import CurrentUser
from app.schemas.case import CaseDetailResponse
from app.services.cases import CaseService
from app.utils.pagination import Page, PageParams, pagination_params

router = APIRouter()


@router.get("", response_model=Page[dict[str, Any]])
def search_cases(
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("case:read"))],
    page: Annotated[PageParams, Depends(pagination_params)],
    q: str | None = Query(default=None),
) -> Page[dict[str, Any]]:
    return CaseService(db).search(page, q=q, filters={})


@router.get("/{case_id}", response_model=CaseDetailResponse)
def get_case(
    case_id: str,
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("case:read"))],
) -> CaseDetailResponse:
    return CaseService(db).detail(case_id)

