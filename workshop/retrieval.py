"""Separate LanceDB retrieval adapter; CrewAI Knowledge still uses its own store."""

from __future__ import annotations

import os
import json
from functools import lru_cache
from pathlib import Path

from crewai.tools import tool

from workshop.common import DATA, ensure_runtime
from workshop.tools import DOCUMENTS


def _embed(text: str) -> list[float]:
    from ollama import Client

    host = os.getenv("WORKSHOP_MODEL_BASE_URL", "http://localhost:11434")
    model = os.getenv("WORKSHOP_EMBEDDING_MODEL", "nomic-embed-text")
    return Client(host=host).embed(model=model, input=text).embeddings[0]


@lru_cache(maxsize=4)
def index_documents(path: Path | None = None) -> int:
    """Rebuild a small teaching index from the three fictional documents."""
    import lancedb

    location = path or ensure_runtime() / "lancedb-rag"
    db = lancedb.connect(str(location))
    rows = []
    for name in DOCUMENTS:
        content = (DATA / name).read_text(encoding="utf-8")
        rows.append({"source_id": name, "content": content, "vector": _embed(content)})
    db.create_table("company_documents", data=rows, mode="overwrite")
    return len(rows)


def search_index(query: str, *, path: Path | None = None, limit: int = 2) -> list[dict[str, str]]:
    if not query.strip() or limit < 1:
        raise ValueError("query must be nonempty and limit positive")
    import lancedb

    location = path or ensure_runtime() / "lancedb-rag"
    table = lancedb.connect(str(location)).open_table("company_documents")
    rows = table.search(_embed(query)).limit(limit).to_list()
    return [{"source_id": row["source_id"], "content": row["content"]} for row in rows]


@tool("Search LanceDB company index")
def lancedb_search_tool(query: str) -> str:
    """Retrieve source-labeled passages from the separate LanceDB workshop index."""
    return json.dumps(search_index(query))
