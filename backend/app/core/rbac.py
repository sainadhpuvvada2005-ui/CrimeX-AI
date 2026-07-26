from enum import Enum


class Role(str, Enum):
    SUPER_ADMIN = "super_admin"
    COMMAND_OFFICER = "command_officer"
    DISTRICT_OFFICER = "district_officer"
    STATION_OFFICER = "station_officer"
    INVESTIGATOR = "investigator"
    ANALYST = "analyst"
    REPORT_VIEWER = "report_viewer"
    AUDITOR = "auditor"


ROLE_PERMISSIONS: dict[Role, set[str]] = {
    Role.SUPER_ADMIN: {"*"},
    Role.COMMAND_OFFICER: {
        "dashboard:read",
        "case:read",
        "victim:read",
        "accused:read",
        "analytics:read",
        "prediction:run",
        "report:create",
        "voice:use",
        "chatbot:use",
        "neo4j:read",
    },
    Role.DISTRICT_OFFICER: {
        "dashboard:read",
        "case:read",
        "victim:read",
        "accused:read",
        "analytics:read",
        "prediction:run",
        "report:create",
        "chatbot:use",
        "neo4j:read",
    },
    Role.STATION_OFFICER: {
        "dashboard:read",
        "case:read",
        "victim:read",
        "accused:read",
        "analytics:read",
        "report:create",
        "chatbot:use",
    },
    Role.INVESTIGATOR: {
        "case:read",
        "victim:read",
        "accused:read",
        "report:create",
        "voice:use",
        "chatbot:use",
        "neo4j:read",
    },
    Role.ANALYST: {
        "dashboard:read",
        "case:read",
        "analytics:read",
        "prediction:run",
        "report:create",
        "chatbot:use",
        "neo4j:read",
    },
    Role.REPORT_VIEWER: {"dashboard:read", "report:create"},
    Role.AUDITOR: {"audit:read", "dashboard:read"},
}


def has_permission(role: str, permission: str) -> bool:
    try:
        role_value = Role(role)
    except ValueError:
        return False
    permissions = ROLE_PERMISSIONS.get(role_value, set())
    return "*" in permissions or permission in permissions

