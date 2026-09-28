"""Exercise CrewAI Flow routing without depending on model output."""

from types import SimpleNamespace

from workshop import decision_flow
from workshop.schemas import DecisionReport, Evidence


def good_report() -> DecisionReport:
    return DecisionReport(
        recommendation="pilot",
        rationale="A pilot is reasonable while deletion and throughput remain unverified.",
        evidence=[
            Evidence(source_id="architecture.md", claim="Private deployment is possible."),
            Evidence(source_id="security.md", claim="Deletion guarantees are not verified."),
        ],
    )


def test_success_and_pending_approval(monkeypatch) -> None:
    class FakeCrew:
        def kickoff(self, inputs):
            assert inputs["question"]
            return SimpleNamespace(pydantic=good_report())

    monkeypatch.setattr(decision_flow, "build_research_crew", lambda: FakeCrew())
    flow = decision_flow.DecisionFlow()
    result = flow.kickoff(inputs={
        "question": "Should Northstar AI pilot Meridian AI?",
        "request_email": True,
        "approved": False,
    })
    assert "PENDING_APPROVAL" in result
    assert flow.state.report is not None
    assert flow.state.retry_count == 0
    assert flow.state.action_result == ""


def test_evidence_failure_is_bounded(monkeypatch) -> None:
    attempts = 0

    class FakeCrew:
        def kickoff(self, inputs):
            nonlocal attempts
            attempts += 1
            return SimpleNamespace(pydantic=None)

    monkeypatch.setattr(decision_flow, "build_research_crew", lambda: FakeCrew())
    flow = decision_flow.DecisionFlow()
    result = flow.kickoff(inputs={"question": "Should Northstar AI pilot Meridian AI?"})
    assert "INSUFFICIENT_EVIDENCE" in result
    assert attempts == 2
    assert flow.state.retry_count == 2


def test_approved_action_uses_unique_flow_id(monkeypatch) -> None:
    class FakeCrew:
        def kickoff(self, inputs):
            return SimpleNamespace(pydantic=good_report())

    actions: list[tuple[bool, str]] = []
    monkeypatch.setattr(decision_flow, "build_research_crew", lambda: FakeCrew())
    monkeypatch.setattr(
        decision_flow,
        "mock_email",
        lambda report, *, approved, action_id: actions.append((approved, action_id)) or "RECORDED",
    )
    flow = decision_flow.DecisionFlow()
    assert flow.kickoff(inputs={
        "question": "Should Northstar AI pilot Meridian AI?",
        "request_email": True,
        "approved": True,
    }) == "RECORDED"
    assert actions == [(True, flow.state.id)]
    assert flow.state.id
