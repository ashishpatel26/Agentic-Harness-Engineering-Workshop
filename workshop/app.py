"""Thin application boundary: memory context in, Flow result out."""

from __future__ import annotations

from workshop.decision_flow import DecisionFlow
from workshop.memory import build_memory, recall_constraints, remember_constraint


def run_assistant(
    *,
    question: str,
    customer_id: str,
    remember: str | None = None,
    request_email: bool = False,
    approved: bool = False,
) -> tuple[DecisionFlow, str]:
    memory = build_memory()
    if remember:
        remember_constraint(memory, customer_id, remember)
    constraints = recall_constraints(memory, customer_id, question)
    flow = DecisionFlow()
    result = flow.kickoff(inputs={
        "question": question,
        "customer_id": customer_id,
        "customer_context": "\n".join(constraints) or "No saved customer constraint.",
        "request_email": request_email,
        "approved": approved,
    })
    return flow, result
