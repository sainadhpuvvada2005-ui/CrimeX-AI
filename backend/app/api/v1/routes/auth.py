from fastapi import APIRouter

from app.api.deps import DbSession
from app.schemas.auth import LoginRequest, LogoutRequest, RefreshTokenRequest, TokenResponse
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: DbSession) -> TokenResponse:
    return AuthService(db).login(payload)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest, db: DbSession) -> TokenResponse:
    return AuthService(db).refresh(payload)


@router.post("/logout")
def logout(payload: LogoutRequest, db: DbSession) -> dict[str, bool]:
    return AuthService(db).logout(payload.access_token)

