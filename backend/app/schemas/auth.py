from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str
    role: str | None = None
    mfa_code: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    access_token: str


class LogoutRequest(BaseModel):
    access_token: str


class CurrentUser(BaseModel):
    user_id: str
    role: str
    unit_code: str | None = None
    district_code: str | None = None
    jurisdiction_scope: dict = Field(default_factory=dict)

class SessionResponse(BaseModel):
    session_id: str
    user_id: str
    role_code: str
    is_active: bool

