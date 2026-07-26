import time
from collections.abc import MutableMapping
from typing import Any


class CatalystCache(MutableMapping[str, Any]):
    """A simple in-process cache with TTL semantics for Catalyst Cache."""

    def __init__(self, ttl_seconds: int = 300) -> None:
        self.ttl_seconds = ttl_seconds
        self._store: dict[str, tuple[float, Any]] = {}

    def _purge_expired(self) -> None:
        now = time.time()
        expired = [key for key, (stored_at, _) in self._store.items() if now - stored_at > self.ttl_seconds]
        for key in expired:
            del self._store[key]

    def __getitem__(self, key: str) -> Any:
        self._purge_expired()
        _, value = self._store[key]
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        self._store[key] = (time.time(), value)

    def __delitem__(self, key: str) -> None:
        del self._store[key]

    def __iter__(self):
        self._purge_expired()
        return iter(self._store)

    def __len__(self) -> int:
        self._purge_expired()
        return len(self._store)
