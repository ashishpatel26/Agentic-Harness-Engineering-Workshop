"""Explicit opt-in CrewAI instrumentation for a configured Langfuse project."""

from __future__ import annotations

import os
from functools import lru_cache


@lru_cache(maxsize=1)
def enable_langfuse() -> bool:
    if os.getenv("WORKSHOP_LANGFUSE_ENABLED", "false").lower() != "true":
        return False
    if not os.getenv("LANGFUSE_PUBLIC_KEY") or not os.getenv("LANGFUSE_SECRET_KEY"):
        raise ValueError("Langfuse tracing enabled without project keys")
    from langfuse import get_client
    from openinference.instrumentation.crewai import CrewAIInstrumentor

    client = get_client()
    if not client.auth_check():
        raise RuntimeError("Langfuse authentication failed")
    # This instrumentation can export prompts and customer data. Opt-in only.
    CrewAIInstrumentor().instrument(skip_dep_check=True)
    return True
