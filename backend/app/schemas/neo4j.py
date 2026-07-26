from typing import Any

from pydantic import BaseModel, Field


class NetworkSearchRequest(BaseModel):
    entity_id: str
    depth: int = Field(default=2, ge=1, le=4)


class NetworkResponse(BaseModel):
    nodes: list[dict[str, Any]]
    relationships: list[dict[str, Any]]

