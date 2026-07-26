from __future__ import annotations

from fastapi import HTTPException, Request, status

from app.core.config import settings
from app.core.security import decode_access_token


class CatalystApiGateway:
    """A lightweight request security policy layer for Catalyst API Gateway."""

    def __init__(self) -> None:
        self.enabled = settings.catalyst_enabled

    async def validate_request(self, request: Request) -> None:
        if not self.enabled:
            return
        auth_header = request.headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
        token = auth_header.split(" ", 1)[1]
        try:
            decode_access_token(token)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token") from exc
