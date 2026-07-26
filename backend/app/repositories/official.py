from __future__ import annotations

from typing import Any

from sqlalchemy import Select, and_, cast, func, or_, select, String
from sqlalchemy.orm import Session

from app.models.official import get_official_table
from app.utils.pagination import PageParams
from app.utils.query import paginate_query


class OfficialTableRepository:
    def __init__(self, db: Session, table_name: str):
        self.db = db
        self.table = get_official_table(db, table_name)

    def list(
        self,
        page: PageParams,
        search: str | None = None,
        filters: dict[str, Any] | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        query = select(self.table)
        query = self._apply_filters(query, filters or {})
        query = self._apply_search(query, search)
        rows, total = paginate_query(self.db, query, page)
        return [dict(row) for row in rows], total

    def get_by_primary_key(self, value: str) -> dict[str, Any] | None:
        pk_cols = list(self.table.primary_key.columns)
        if not pk_cols:
            return None
        pk_col = pk_cols[0]
        query = select(self.table).where(cast(pk_col, String) == value).limit(1)
        row = self.db.execute(query).mappings().first()
        return dict(row) if row else None

    def count(self) -> int:
        return self.db.execute(select(func.count()).select_from(self.table)).scalar_one()

    def aggregate(self, dimension: str, filters: dict[str, Any] | None = None, limit: int = 25) -> list[dict[str, Any]]:
        if dimension not in self.table.c:
            raise ValueError(f"Unsupported dimension for {self.table.name}: {dimension}")
        dimension_col = self.table.c[dimension]
        query = (
            select(dimension_col.label("dimension"), func.count().label("count"))
            .select_from(self.table)
            .group_by(dimension_col)
            .order_by(func.count().desc())
            .limit(limit)
        )
        query = self._apply_filters(query, filters or {})
        return [dict(row) for row in self.db.execute(query).mappings().all()]

    def _apply_filters(self, query: Select, filters: dict[str, Any]) -> Select:
        predicates = []
        for field, value in filters.items():
            if field not in self.table.c or value is None:
                continue
            column = self.table.c[field]
            if isinstance(value, list):
                predicates.append(column.in_(value))
            else:
                predicates.append(cast(column, String) == str(value))
        return query.where(and_(*predicates)) if predicates else query

    def _apply_search(self, query: Select, search: str | None) -> Select:
        if not search:
            return query
        predicates = [cast(column, String).ilike(f"%{search}%") for column in self.table.c]
        return query.where(or_(*predicates))

