from fastapi import APIRouter

from app.core.config import settings
from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="crimex-api",
        version="1.0.0",
        metadata={
            "catalyst_enabled": settings.catalyst_enabled,
            "environment": settings.environment,
            "catalyst_namespace": settings.catalyst_namespace,
        },
    )

