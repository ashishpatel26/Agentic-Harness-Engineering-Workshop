"""Pure Python functions plus CrewAI tool wrappers."""

from __future__ import annotations

import json
import re

from crewai.tools import tool

from workshop.common import DATA

DOCUMENTS = ("architecture.md", "security.md", "pricing.md")


def calculate_annual_roi(annual_benefit: float, annual_cost: float) -> float:
    """Return a planning-scenario percentage, with validated inputs."""
    if annual_benefit < 0 or annual_cost <= 0:
        raise ValueError("benefit must be non-negative and cost must be positive")
    return round((annual_benefit - annual_cost) / annual_cost * 100, 1)


def search_documents(query: str, limit: int = 2) -> list[dict[str, str]]:
    """Transparent keyword search used before the Knowledge/RAG lesson."""
    if not query.strip():
        raise ValueError("query must not be empty")
    terms = set(re.findall(r"[a-z]{3,}", query.lower()))
    matches = []
    for name in DOCUMENTS:
        content = (DATA / name).read_text(encoding="utf-8")
        score = sum(term in content.lower() for term in terms)
        matches.append((score, name, content))
    matches.sort(key=lambda item: (-item[0], item[1]))
    return [
        {"source_id": name, "content": content[:1200]}
        for score, name, content in matches[:limit]
        if score > 0
    ]


@tool("Calculate annual ROI")
def roi_tool(annual_benefit: float, annual_cost: float) -> str:
    """Calculate a hypothetical annual ROI percentage from stated USD assumptions."""
    from workshop.cache import cached_annual_roi

    value = cached_annual_roi(annual_benefit, annual_cost)
    return json.dumps({"roi_percent": value, "status": "scenario, not a guarantee"})


@tool("Search company documents")
def company_search_tool(query: str) -> str:
    """Find relevant passages in Northstar's three fictional workshop documents."""
    return json.dumps(search_documents(query))


@tool("Search research fixture")
def research_tool(query: str) -> str:
    """Return a fixed external-research fixture; this tool never accesses the web."""
    if not query.strip():
        raise ValueError("query must not be empty")
    return json.dumps({
        "source_id": "research-fixture",
        "note": "Meridian AI feature claims are unverified workshop assumptions. "
        "Validate throughput, retention, deletion, and pilot price with the vendor.",
    })
