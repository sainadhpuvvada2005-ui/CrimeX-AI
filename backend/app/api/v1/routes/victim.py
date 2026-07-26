from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.deps import DbSession, require_permission
from app.schemas.auth import CurrentUser
from app.services.cases import OfficialEntityService
from app.utils.pagination import Page, PageParams, pagination_params

router = APIRouter()


@router.get("", response_model=Page[dict[str, Any]])
def search_victims(
    db: DbSession,
    user: Annotated[CurrentUser, Depends(require_permission("victim:read"))],
    page: Annotated[PageParams, Depends(pagination_params)],
    q: str | None = Query(default=None),
) -> Page[dict[str, Any]]:
    return OfficialEntityService(db, "Victim").search(page, q=q, filters={})

