from __future__ import annotations

from typing import Any

from app.integrations.catalyst.nosql import CatalystNoSQL


class CatalystNotifications:
    """A simple notification adapter for web and mobile delivery."""

    def __init__(self, nosql: CatalystNoSQL | None = None) -> None:
        self.nosql = nosql or CatalystNoSQL()

    def send(self, channel: str, message: str, *, metadata: dict[str, Any] | None = None) -> str:
        return self.nosql.write("notifications", {"channel": channel, "message": message, **(metadata or {})})
