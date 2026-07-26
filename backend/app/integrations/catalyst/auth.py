from __future__ import annotations

from typing import Any

from app.core.rbac import Role
from app.core.security import create_access_token
from app.integrations.catalyst.data_store import CatalystDataStore


class CatalystAuthService:
    """A thin Catalyst authentication adapter for the existing auth flow."""

    def __init__(self, datastore: CatalystDataStore | None = None) -> None:
        self.datastore = datastore or CatalystDataStore(namespace="crimex")

    def issue_session(self, username: str, password: str, *, role: str | None = None) -> dict[str, Any]:
        if password != "dev-password":
            raise ValueError("Invalid credentials")

        resolved_role = role or self._default_role(username)
        if resolved_role not in {member.value for member in Role}:
            resolved_role = Role.INVESTIGATOR.value

        session_id = self.datastore.save(
            "sessions",
            {
                "user": username,
                "role": resolved_role,
                "is_active": True,
                "auth_provider": "catalyst",
            },
        )
        claims = {
            "sub": username,
            "role": resolved_role,
            "session_id": session_id,
            "unit_code": None,
            "district_code": None,
            "jurisdiction_scope": {},
            "permissions": self._permissions_for(resolved_role),
        }
        token = create_access_token(username, claims)
        claims["access_token"] = token
        claims["refresh_token"] = token
        return claims

    def invalidate_session(self, session_id: str | None) -> None:
        if not session_id:
            return
        self.datastore.save(
            "sessions",
            {
                "id": session_id,
                "is_active": False,
                "auth_provider": "catalyst",
            },
        )

    def _default_role(self, username: str) -> str:
        return Role.SUPER_ADMIN.value if username == "admin" else Role.INVESTIGATOR.value

    def _permissions_for(self, role: str) -> list[str]:
        permissions_map = {
            Role.SUPER_ADMIN.value: ["*"],
            Role.COMMAND_OFFICER.value: ["dashboard:read", "case:read", "analytics:read", "prediction:run"],
            Role.DISTRICT_OFFICER.value: ["dashboard:read", "case:read", "analytics:read"],
            Role.STATION_OFFICER.value: ["dashboard:read", "case:read"],
            Role.INVESTIGATOR.value: ["case:read", "voice:use", "chatbot:use"],
            Role.ANALYST.value: ["dashboard:read", "analytics:read", "prediction:run"],
            Role.REPORT_VIEWER.value: ["dashboard:read", "report:create"],
            Role.AUDITOR.value: ["audit:read"],
        }
        return permissions_map.get(role, ["case:read"])
