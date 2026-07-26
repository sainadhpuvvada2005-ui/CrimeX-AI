from __future__ import annotations

from typing import Any

from app.integrations.catalyst.nosql import CatalystNoSQL


class CatalystSignals:
    """Lightweight event handlers that mirror Catalyst Signals behavior."""

    def __init__(self, nosql: CatalystNoSQL | None = None) -> None:
        self.nosql = nosql or CatalystNoSQL()

    def emit(self, event_name: str, payload: dict[str, Any]) -> str:
        return self.nosql.write("ai_logs", {"event": event_name, **payload})
