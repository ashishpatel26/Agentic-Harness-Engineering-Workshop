"""Deterministic boundaries around the agent's recommendation and actions."""

from __future__ import annotations

import json
from pathlib import Path

from workshop.common import ensure_runtime
from workshop.schemas import DecisionReport
from workshop.tools import DOCUMENTS


def validate_question(question: str) -> str:
    cleaned = question.strip()
    if len(cleaned) < 12 or len(cleaned) > 500:
        raise ValueError("question must contain 12–500 characters")
    return cleaned


def validate_report(report: DecisionReport) -> tuple[bool, str]:
    sources = {item.source_id for item in report.evidence}
    unknown = sources.difference(DOCUMENTS)
    if unknown:
        return False, f"Unknown source IDs: {sorted(unknown)}"
    if len(sources) < 2:
        return False, "At least two distinct internal documents are required"
    if len(report.rationale.strip()) < 30:
        return False, "Rationale is too short to audit"
    return True, "Evidence check passed"


def mock_email(report: DecisionReport, *, approved: bool, action_id: str) -> str:
    """Write an idempotent local action record; never send a real email."""
    if not approved:
        return "BLOCKED: human approval is required"
    path: Path = ensure_runtime() / "mock-email-actions.jsonl"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if json.loads(line)["action_id"] == action_id:
                return "ALREADY_RECORDED: action was not repeated"
    record = {"action_id": action_id, "recommendation": report.recommendation}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
    return "RECORDED: mock email action only"
