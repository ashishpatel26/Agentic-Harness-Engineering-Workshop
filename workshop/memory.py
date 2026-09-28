"""Scoped CrewAI Memory; customer scope is always explicit."""

from crewai import Memory

from workshop.common import embedder_config


def build_memory() -> Memory:
    return Memory(embedder=embedder_config())


def customer_scope(customer_id: str) -> str:
    if not customer_id or not customer_id.replace("-", "").isalnum():
        raise ValueError("customer_id must contain only letters, digits, or hyphens")
    return f"/customer/{customer_id.lower()}"


def remember_constraint(memory: Memory, customer_id: str, fact: str) -> None:
    memory.remember(fact, scope=customer_scope(customer_id), source=f"customer:{customer_id}")


def recall_constraints(memory: Memory, customer_id: str, question: str) -> list[str]:
    matches = memory.recall(question, scope=customer_scope(customer_id), limit=3)
    return [match.record.content for match in matches]
