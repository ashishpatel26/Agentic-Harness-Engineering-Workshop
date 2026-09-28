"""Pure request builder shared by UI lesson and Streamlit client."""

from workshop.api import DecisionRequest


def decision_payload(customer_id: str, question: str, *, remember: str | None = None,
                     request_email: bool = False) -> dict[str, object]:
    return DecisionRequest(customer_id=customer_id, question=question,
                           remember=remember, request_email=request_email).model_dump()
