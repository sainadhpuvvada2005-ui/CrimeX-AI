from __future__ import annotations

from typing import Any

from app.integrations.catalyst.cache import CatalystCache
from app.integrations.catalyst.nosql import CatalystNoSQL


class CatalystQuickML:
    """A lightweight RAG and prompt-template adapter for Catalyst QuickML."""

    def __init__(self, cache: CatalystCache | None = None, nosql: CatalystNoSQL | None = None) -> None:
        self.cache = cache or CatalystCache(ttl_seconds=600)
        self.nosql = nosql or CatalystNoSQL()

    def retrieve(self, query: str) -> list[dict[str, Any]]:
        cached = self.cache.get(query) if query in self.cache else None
        if cached is not None:
            return cached
        documents = [
            {"source": "official_erd", "content": "Use official FIR schema and approved views only."},
            {"source": "sop", "content": "Use evidence-based answers with citations and confidence."},
        ]
        self.cache[query] = documents
        return documents

    def save_conversation(self, *, session_id: str, prompt: str, response: str) -> str:
        return self.nosql.write("chat_history", {"session_id": session_id, "prompt": prompt, "response": response})
