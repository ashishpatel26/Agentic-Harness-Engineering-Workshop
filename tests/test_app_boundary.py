"""The end-to-end entry point passes scoped memory into the CrewAI Flow."""

from workshop import app


def test_run_assistant_passes_customer_context(monkeypatch) -> None:
    calls = []

    class FakeFlow:
        def kickoff(self, *, inputs):
            calls.append(inputs)
            return "report ready"

    memory = object()
    monkeypatch.setattr(app, "build_memory", lambda: memory)
    monkeypatch.setattr(app, "remember_constraint", lambda store, customer, fact: calls.append((store, customer, fact)))
    monkeypatch.setattr(app, "recall_constraints", lambda store, customer, question: ["Private VPC required"])
    monkeypatch.setattr(app, "DecisionFlow", FakeFlow)

    flow, output = app.run_assistant(
        question="Should Northstar AI pilot Meridian AI?",
        customer_id="customer-a",
        remember="Private VPC required",
        request_email=True,
        approved=False,
    )
    assert isinstance(flow, FakeFlow)
    assert output == "report ready"
    assert calls[0] == (memory, "customer-a", "Private VPC required")
    assert calls[1]["customer_context"] == "Private VPC required"
    assert calls[1]["request_email"] is True
    assert calls[1]["approved"] is False
