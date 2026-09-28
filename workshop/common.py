"""Shared settings and paths for the CrewAI workshop."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
WORKSHOP = Path(__file__).resolve().parent
DATA = WORKSHOP / "data"
RUNTIME = WORKSHOP / ".workshop-data"
load_dotenv(ROOT / ".env")


def model():
    """Use an explicit model; never silently fall back to a paid provider."""
    from crewai import LLM

    name = os.getenv("WORKSHOP_MODEL", "ollama/qwen3.5:4b")
    settings: dict[str, object] = {"model": name, "temperature": 0}
    if name.startswith("ollama/"):
        settings["base_url"] = os.getenv("WORKSHOP_MODEL_BASE_URL", "http://localhost:11434")
    return LLM(**settings)


def embedder_config() -> dict[str, object]:
    """Knowledge and Memory need a separately configured embedding model."""
    provider = os.getenv("WORKSHOP_EMBEDDING_PROVIDER", "ollama")
    if provider == "ollama":
        return {
            "provider": provider,
            "config": {
                "model_name": os.getenv("WORKSHOP_EMBEDDING_MODEL", "nomic-embed-text"),
                "url": os.getenv("WORKSHOP_OLLAMA_EMBED_URL", "http://localhost:11434/api/embeddings"),
            },
        }
    if provider == "openai":
        return {
            "provider": provider,
            "config": {"model_name": os.getenv("WORKSHOP_EMBEDDING_MODEL", "text-embedding-3-small")},
        }
    raise ValueError(f"Unsupported workshop embedding provider: {provider}")


def ensure_runtime() -> Path:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    return RUNTIME
