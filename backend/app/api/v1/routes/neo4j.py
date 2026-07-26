from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import require_permission
from app.schemas.auth import CurrentUser
from app.schemas.neo4j import NetworkResponse, NetworkSearchRequest
from app.services.neo4j import Neo4jService

router = APIRouter()


@router.post("/network", response_model=NetworkResponse)
def network(
    payload: NetworkSearchRequest,
    user: Annotated[CurrentUser, Depends(require_permission("neo4j:read"))],
) -> NetworkResponse:
    return Neo4jService().network(payload.entity_id, payload.depth)

