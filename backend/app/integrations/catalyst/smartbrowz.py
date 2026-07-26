from __future__ import annotations

from typing import Any

from app.integrations.catalyst.storage import CatalystStratus


class CatalystSmartBrowz:
    """Report generation helper for Catalyst SmartBrowz."""

    def __init__(self, storage: CatalystStratus | None = None) -> None:
        self.storage = storage or CatalystStratus()

    def generate_report(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        return {"name": name, "payload": payload, "status": "generated"}
