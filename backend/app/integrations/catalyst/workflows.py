from __future__ import annotations

from typing import Any

from app.integrations.catalyst.nosql import CatalystNoSQL


class CatalystCircuits:
    """Minimal workflow orchestration helper for investigation and reporting workflows."""

    def __init__(self, nosql: CatalystNoSQL | None = None) -> None:
        self.nosql = nosql or CatalystNoSQL()

    def start(self, workflow_name: str, payload: dict[str, Any]) -> str:
        return self.nosql.write("activity_logs", {"workflow": workflow_name, **payload})
