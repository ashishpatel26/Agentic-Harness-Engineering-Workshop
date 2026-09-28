"""Checks for deterministic boundaries that should not depend on an LLM."""

import json
from pathlib import Path

import pytest

from workshop import control
from workshop.common import embedder_config
from workshop.memory import customer_scope
from workshop.schemas import DecisionReport, Evidence
from workshop.tools import calculate_annual_roi, search_documents


def report() -> DecisionReport:
    return DecisionReport(
        recommendation="pilot",
        rationale="A pilot is reasonable while security and scale unknowns are verified.",
        evidence=[
            Evidence(source_id="architecture.md", claim="Private deployment is possible."),
            Evidence(source_id="security.md", claim="Deletion terms are unknown."),
        ],
    )


def test_roi_contract() -> None:
    assert calculate_annual_roi(45_000, 30_000) == 50.0
    with pytest.raises(ValueError):
        calculate_annual_roi(45_000, 0)


def test_source_ids_and_question_validation() -> None:
    assert control.validate_report(report())[0]
    bad = report().model_copy(update={"evidence": [Evidence(source_id="made-up.pdf", claim="Claim")]} )
    assert not control.validate_report(bad)[0]
    with pytest.raises(ValueError):
        control.validate_question("hi")


def test_customer_scope_rejects_path_traversal() -> None:
    assert customer_scope("Customer-A") == "/customer/customer-a"
    with pytest.raises(ValueError):
        customer_scope("../other")


def test_mock_action_requires_approval_and_is_idempotent(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(control, "ensure_runtime", lambda: tmp_path)
    assert control.mock_email(report(), approved=False, action_id="case-1").startswith("BLOCKED")
    assert not (tmp_path / "mock-email-actions.jsonl").exists()
    assert control.mock_email(report(), approved=True, action_id="case-1").startswith("RECORDED")
    assert control.mock_email(report(), approved=True, action_id="case-1").startswith("ALREADY_RECORDED")
    records = [json.loads(line) for line in (tmp_path / "mock-email-actions.jsonl").read_text().splitlines()]
    assert len(records) == 1


def test_document_search_returns_real_source_ids() -> None:
    matches = search_documents("private VPC deployment")
    assert matches and matches[0]["source_id"] == "architecture.md"


def test_embedding_provider_is_explicit(monkeypatch) -> None:
    monkeypatch.setenv("WORKSHOP_EMBEDDING_PROVIDER", "openai")
    monkeypatch.setenv("WORKSHOP_EMBEDDING_MODEL", "text-embedding-3-small")
    assert embedder_config() == {
        "provider": "openai",
        "config": {"model_name": "text-embedding-3-small"},
    }
    monkeypatch.setenv("WORKSHOP_EMBEDDING_PROVIDER", "unknown")
    with pytest.raises(ValueError):
        embedder_config()


def test_local_embedder_dependency_is_installed(monkeypatch) -> None:
    from crewai.rag.embeddings.factory import build_embedder

    monkeypatch.setenv("WORKSHOP_EMBEDDING_PROVIDER", "ollama")
    assert callable(build_embedder(embedder_config()))
