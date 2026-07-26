from __future__ import annotations

from pathlib import Path
from typing import Any


class CatalystDeploymentGuide:
    """Produces deployment guidance and environment variable templates for Catalyst."""

    def __init__(self, target_dir: str | None = None) -> None:
        self.target_dir = Path(target_dir or Path(__file__).resolve().parents[2])

    def write_config(self) -> Path:
        content = """# Catalyst environment configuration\nCATALYST_ENABLED=true\nCATALYST_NAMESPACE=crimex\nCATALYST_STORAGE_ROOT=.catalyst\nDATABASE_URL=sqlite:///./crimex_local.db\nJWT_SECRET_KEY=change-me\nMFA_REQUIRED=false\n"""
        path = self.target_dir / ".env.catalyst"
        path.write_text(content, encoding="utf-8")
        return path

    def build_manifest(self) -> dict[str, Any]:
        return {
            "services": [
                "auth",
                "data-store",
                "nosql",
                "stratus",
                "cache",
                "quickml",
                "zia",
                "signals",
                "circuits",
                "cron",
                "push",
                "mail",
            ],
            "deployment": "app-sail",
            "domain": "https://crimex.example.gov",
        }
