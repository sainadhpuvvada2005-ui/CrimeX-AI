from __future__ import annotations

from typing import Any

from app.integrations.catalyst.nosql import CatalystNoSQL


class CatalystMail:
    """Email and notification adapter for OTPs, resets, and report delivery."""

    def __init__(self, nosql: CatalystNoSQL | None = None) -> None:
        self.nosql = nosql or CatalystNoSQL()

    def send(self, template: str, recipient: str, *, metadata: dict[str, Any] | None = None) -> str:
        return self.nosql.write("notifications", {"template": template, "recipient": recipient, **(metadata or {})})
