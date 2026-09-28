"""Offline checks for the optional API, cache, NeMo, and retrieval boundaries."""

from __future__ import annotations

import os
from types import SimpleNamespace
from uuid import uuid4

import pytest


def test_api_requires_tokens_and_does_not_accept_self_approval(monkeypatch) -> None:
    pytest.importorskip("fastapi")
    from fastapi import HTTPException
    from pydantic import ValidationError
    from workshop import api as module

    monkeypatch.setenv("WORKSHOP_API_TOKEN", "demo-api-token")
    monkeypatch.setenv("WORKSHOP_APPROVAL_TOKEN", "demo-instructor-token")
    monkeypatch.setattr(module, "configured_store", lambda: None)
    calls = []

    def fake_run(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(state=SimpleNamespace(
            id=str(uuid4()), report=None, failure="", action_result=""
        )), "INSUFFICIENT_EVIDENCE: demo"

    monkeypatch.setattr(module, "run_assistant", fake_run)
    payload = {"question": "Should Northstar AI pilot Meridian AI?", "customer_id": "customer-a"}
    assert module.health()["status"] == "ok"
    with pytest.raises(ValidationError):
        module.DecisionRequest.model_validate({**payload, "approved": True})
    with pytest.raises(HTTPException) as denied:
        module.decide(module.DecisionRequest(**payload), x_workshop_api_token=None)
    assert denied.value.status_code == 403
    response = module.decide(module.DecisionRequest(**payload),
                             x_workshop_api_token="demo-api-token")
    assert calls[0]["approved"] is False
    assert response.report is None
    with pytest.raises(HTTPException) as denied:
        module.approve(uuid4(), x_workshop_approval_token=None)
    assert denied.value.status_code == 403
    with pytest.raises(HTTPException) as missing_store:
        module.approve(uuid4(), x_workshop_approval_token="demo-instructor-token")
    assert missing_store.value.status_code == 503


def test_cache_is_optional_and_does_not_bypass_validation(monkeypatch) -> None:
    from workshop.cache import cached_annual_roi

    monkeypatch.delenv("WORKSHOP_REDIS_URL", raising=False)
    assert cached_annual_roi(45_000, 30_000) == 50.0
    with pytest.raises(ValueError):
        cached_annual_roi(45_000, 0)


def test_nemo_disabled_by_default_and_rejects_empty_when_enabled(monkeypatch) -> None:
    from workshop import nemo_guardrails

    monkeypatch.setenv("WORKSHOP_NEMO_ENABLED", "false")
    nemo_guardrails.check_input("safe")
    monkeypatch.setenv("WORKSHOP_NEMO_ENABLED", "true")
    with pytest.raises(ValueError, match="empty"):
        nemo_guardrails.check_input(" ")
    with pytest.raises(ValueError, match="empty"):
        nemo_guardrails.check_output("question", " ")


def test_ragas_fixture_is_versioned_and_named() -> None:
    from workshop.ragas_eval import load_cases

    cases = load_cases()
    assert len(cases) >= 2
    assert len({case["id"] for case in cases}) == len(cases)


def test_lancedb_adapter_returns_only_source_ids(monkeypatch, tmp_path) -> None:
    if os.getenv("WORKSHOP_INTEGRATION_TESTS") != "1":
        pytest.skip("Set WORKSHOP_INTEGRATION_TESTS=1 outside the restricted sandbox")
    pytest.importorskip("lancedb")
    from workshop import retrieval
    from workshop.tools import DOCUMENTS

    def vector(text: str) -> list[float]:
        lower = text.lower()
        return [float("private" in lower), float("deletion" in lower), 0.1]

    monkeypatch.setattr(retrieval, "_embed", vector)
    assert retrieval.index_documents(tmp_path / "index") == len(DOCUMENTS)
    results = retrieval.search_index("private deployment", path=tmp_path / "index")
    assert results and all(item["source_id"] in DOCUMENTS for item in results)
    with pytest.raises(ValueError):
        retrieval.search_index(" ", path=tmp_path / "index")


def test_http_boundary_smoke(monkeypatch) -> None:
    if os.getenv("WORKSHOP_INTEGRATION_TESTS") != "1":
        pytest.skip("Set WORKSHOP_INTEGRATION_TESTS=1 outside the restricted sandbox")
    from fastapi.testclient import TestClient
    from workshop import api as module

    monkeypatch.setenv("WORKSHOP_API_TOKEN", "integration-token")
    monkeypatch.delenv("WORKSHOP_DATABASE_URL", raising=False)
    monkeypatch.delenv("WORKSHOP_REDIS_URL", raising=False)
    monkeypatch.setattr(module, "configured_store", lambda: None)
    monkeypatch.setattr(module, "run_assistant", lambda **kwargs: (
        SimpleNamespace(state=SimpleNamespace(id=str(uuid4()), report=None, failure="", action_result="")),
        "INSUFFICIENT_EVIDENCE: fixture",
    ))
    client = TestClient(module.api)
    assert client.get("/health").status_code == 200
    assert client.post("/decisions", json={
        "question": "Should Northstar AI pilot Meridian AI?", "customer_id": "customer-a"
    }).status_code == 403
    response = client.post("/decisions", headers={"X-Workshop-API-Token": "integration-token"}, json={
        "question": "Should Northstar AI pilot Meridian AI?", "customer_id": "customer-a"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "complete"
