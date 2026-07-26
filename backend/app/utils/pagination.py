from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field


T = TypeVar("T")


class PageParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=25, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class Page(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int


def pagination_params(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=25, ge=1, le=100),
) -> PageParams:
    return PageParams(page=page, size=size)

