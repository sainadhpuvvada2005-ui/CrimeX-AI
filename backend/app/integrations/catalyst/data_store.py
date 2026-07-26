import json
import uuid
from pathlib import Path
from typing import Any


class CatalystDataStore:
    """A lightweight Catalyst-style key/value data-store adapter.

    This provides the same create/get/list/delete contract expected by the
    application while allowing the backend to run locally without a live Zoho
    Catalyst environment. In a real Catalyst deployment this class can be
    swapped to call the appropriate hosted service endpoints.
    """

    def __init__(self, namespace: str = "crimex", storage_root: str | None = None) -> None:
        self.namespace = namespace
        self.storage_root = Path(storage_root or Path(__file__).resolve().parents[2] / ".catalyst")
        self.storage_root.mkdir(parents=True, exist_ok=True)

    def _path(self, collection: str) -> Path:
        return self.storage_root / f"{self.namespace}_{collection}.json"

    def _read_collection(self, collection: str) -> dict[str, dict[str, Any]]:
        path = self._path(collection)
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _write_collection(self, collection: str, payload: dict[str, dict[str, Any]]) -> None:
        self._path(collection).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def save(self, collection: str, payload: dict[str, Any]) -> str:
        record_id = str(payload.get("id") or payload.get("session_id") or uuid.uuid4())
        records = self._read_collection(collection)
        record = dict(payload)
        record["id"] = record_id
        records[record_id] = record
        self._write_collection(collection, records)
        return record_id

    def get(self, collection: str, record_id: str) -> dict[str, Any] | None:
        records = self._read_collection(collection)
        return records.get(record_id)

    def list(self, collection: str) -> list[dict[str, Any]]:
        records = self._read_collection(collection)
        return list(records.values())

    def delete(self, collection: str, record_id: str) -> None:
        records = self._read_collection(collection)
        records.pop(record_id, None)
        self._write_collection(collection, records)
