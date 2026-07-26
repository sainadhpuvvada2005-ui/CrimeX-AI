import json
import uuid
from pathlib import Path
from typing import Any


class CatalystNoSQL:
    """A lightweight Catalyst NoSQL collection adapter used for audit trails and chat history."""

    def __init__(self, storage_root: str | None = None) -> None:
        self.storage_root = Path(storage_root or Path(__file__).resolve().parents[2] / ".catalyst")
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def _path(self, collection: str) -> Path:
        return self.storage_root / f"nosql_{collection}.json"

    def _read(self, collection: str) -> list[dict[str, Any]]:
        path = self._path(collection)
        if not path.exists():
            return []
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []

    def _write(self, collection: str, documents: list[dict[str, Any]]) -> None:
        self._path(collection).write_text(json.dumps(documents, indent=2, sort_keys=True), encoding="utf-8")

    def write(self, collection: str, payload: dict[str, Any]) -> str:
        documents = self._read(collection)
        record = dict(payload)
        record.setdefault("id", str(uuid.uuid4()))
        documents.append(record)
        self._write(collection, documents)
        return str(record["id"])

    def list(self, collection: str) -> list[dict[str, Any]]:
        return self._read(collection)

    def get(self, collection: str, record_id: str) -> dict[str, Any] | None:
        return next((doc for doc in self._read(collection) if str(doc.get("id")) == str(record_id)), None)
