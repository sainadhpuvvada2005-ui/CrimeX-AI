from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

try:
    import orjson  # noqa: F401
    from fastapi.responses import ORJSONResponse as DefaultJSONResponse
except ModuleNotFoundError:
    DefaultJSONResponse = JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.integrations.catalyst.gateway import CatalystApiGateway


class CatalystGatewayMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, gateway: CatalystApiGateway | None = None) -> None:
        super().__init__(app)
        self.gateway = gateway or CatalystApiGateway()

    async def dispatch(self, request: Request, call_next) -> Response:
        public_paths = {"/docs", "/redoc", "/openapi.json", "/api/v1/health", "/api/v1/auth/login", "/api/v1/auth/refresh"}
        if request.url.path in public_paths:
            return await call_next(request)
        try:
            await self.gateway.validate_request(request)
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
        return await call_next(request)


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="CrimeX AI backend for conversational crime intelligence, analytics, reports, voice, prediction, and Neo4j network analysis.",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        default_response_class=DefaultJSONResponse,
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(CatalystGatewayMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
