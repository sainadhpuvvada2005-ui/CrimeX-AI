from __future__ import annotations

from typing import Any


class CatalystCron:
    """Declarative cron jobs for sync and refresh tasks."""

    def __init__(self) -> None:
        self.jobs = {
            "daily_sync": "Sync official FIR data and redrive caches.",
            "weekly_analytics": "Refresh analytics aggregates.",
            "monthly_reports": "Generate monthly report snapshots.",
            "neo4j_refresh": "Refresh graph projections.",
            "vector_refresh": "Refresh vector index metadata.",
            "feature_store_refresh": "Refresh prediction features.",
        }

    def list_jobs(self) -> dict[str, Any]:
        return self.jobs
