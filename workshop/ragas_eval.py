"""Opt-in Ragas factual score against a local Ollama model."""

from __future__ import annotations

import os
import json
from pathlib import Path

from workshop.common import model_name


def load_cases() -> list[dict[str, str]]:
    path = Path(__file__).resolve().parent / "evals" / "factual_cases.json"
    cases = json.loads(path.read_text(encoding="utf-8"))
    if not cases or any(not all(case.get(field) for field in ("id", "response", "reference")) for case in cases):
        raise ValueError("Ragas fixture must contain named nonempty response/reference pairs")
    return cases


async def factual_score(response: str, reference: str) -> float:
    """Return a model-judged score; never substitute for deterministic safety tests."""
    if not response.strip() or not reference.strip():
        raise ValueError("response and reference must be nonempty")
    from openai import AsyncOpenAI
    from ragas.llms import llm_factory
    from ragas.metrics.collections import FactualCorrectness

    model = model_name()
    if not model.startswith("ollama/"):
        raise ValueError("This local evaluation example requires Ollama")
    base_url = os.getenv("WORKSHOP_MODEL_BASE_URL", "http://localhost:11434").rstrip("/")
    client = AsyncOpenAI(api_key="ollama", base_url=f"{base_url}/v1")
    evaluator = llm_factory(model.removeprefix("ollama/"), provider="openai", client=client)
    result = await FactualCorrectness(llm=evaluator).ascore(response=response, reference=reference)
    return float(result.value)
