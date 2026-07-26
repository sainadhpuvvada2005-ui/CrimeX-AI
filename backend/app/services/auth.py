from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.rbac import Role
from app.core.security import create_access_token, decode_access_token
from app.integrations.catalyst.auth import CatalystAuthService
from app.integrations.catalyst.data_store import CatalystDataStore
from app.schemas.auth import LoginRequest, RefreshTokenRequest, TokenResponse


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.catalyst_auth = CatalystAuthService(
            CatalystDataStore(namespace=settings.catalyst_namespace, storage_root=settings.catalyst_storage_root)
        )

    def login(self, payload: LoginRequest) -> TokenResponse:
        if settings.catalyst_enabled or settings.environment == "production":
            claims = self.catalyst_auth.issue_session(
                payload.username,
                payload.password,
                role=payload.role if getattr(payload, "role", None) else None,
            )
            return TokenResponse(access_token=claims["access_token"], refresh_token=claims.get("refresh_token"))

        if payload.password != "dev-password":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        role = Role.SUPER_ADMIN.value if payload.username == "admin" else Role.INVESTIGATOR.value
        token = create_access_token(
            payload.username,
            {
                "role": role,
                "session_id": "local",
                "unit_code": None,
                "district_code": None,
                "jurisdiction_scope": {},
            },
        )
        return TokenResponse(access_token=token)

    def refresh(self, payload: RefreshTokenRequest) -> TokenResponse:
        try:
            claims = decode_access_token(payload.access_token)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from exc

        refreshed = create_access_token(
            claims.get("sub", "user"),
            {
                "role": claims.get("role", Role.INVESTIGATOR.value),
                "session_id": claims.get("session_id", "local"),
                "unit_code": claims.get("unit_code"),
                "district_code": claims.get("district_code"),
                "jurisdiction_scope": claims.get("jurisdiction_scope") or {},
                "permissions": claims.get("permissions", []),
            },
        )
        return TokenResponse(access_token=refreshed, refresh_token=payload.access_token)

    def logout(self, token: str) -> dict[str, bool]:
        try:
            claims = decode_access_token(token)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc

        self.catalyst_auth.invalidate_session(claims.get("session_id"))
        return {"success": True}

