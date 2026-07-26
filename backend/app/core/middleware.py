import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.integrations.catalyst.events import CatalystSignals


try:
    import structlog

    logger = structlog.get_logger(__name__)
except ModuleNotFoundError:
    import logging

    logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("x-correlation-id", str(uuid.uuid4()))
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        response.headers["x-correlation-id"] = correlation_id
        try:
            logger.info(
                "http_request",
                correlation_id=correlation_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
            )
            CatalystSignals().emit(
                "http_request",
                {
                    "path": request.url.path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "correlation_id": correlation_id,
                },
            )
        except TypeError:
            logger.info(
                "http_request correlation_id=%s method=%s path=%s status_code=%s duration_ms=%s",
                correlation_id,
                request.method,
                request.url.path,
                response.status_code,
                duration_ms,
            )
        return response
