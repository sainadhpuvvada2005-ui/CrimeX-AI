from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class PipelineStep:
    name: str
    command: str


class CatalystPipelines:
    """Declarative pipeline definitions for CI/CD and deployment automation."""

    def build(self) -> list[PipelineStep]:
        return [
            PipelineStep("install", "pip install -r requirements.txt"),
            PipelineStep("test", "pytest -q"),
            PipelineStep("deploy", "uvicorn app.main:app --host 0.0.0.0 --port 8000"),
        ]

    def deploy(self) -> dict[str, Any]:
        return {"status": "prepared", "steps": [step.name for step in self.build()]}
