"""FastAPI boundary for the advanced track; the CLI and HTTP share run_assistant."""

from __future__ import annotations

import hmac
import os
from uuid import UUID

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator

from workshop.app import run_assistant
from workshop.control import validate_question
from workshop.memory import customer_scope
from workshop.persistence import configured_store
from workshop.schemas import DecisionReport

api = FastAPI(title="Agentic Harness Workshop API", version="0.1.0")


class DecisionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str = Field(min_length=12, max_length=500)
    customer_id: str = Field(min_length=1, max_length=80)
    remember: str | None = Field(default=None, max_length=500)
    request_email: bool = False

    @field_validator("question")
    @classmethod
    def check_question(cls, value: str) -> str:
        return validate_question(value)

    @field_validator("customer_id")
    @classmethod
    def check_customer(cls, value: str) -> str:
        customer_scope(value)
        return value


class DecisionResponse(BaseModel):
    run_id: str
    status: str
    report: DecisionReport | None
    output: str


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@api.get("/ready")
def ready() -> dict[str, str]:
    store = configured_store()
    if store:
        try:
            store.ping()
        except Exception as error:
            raise HTTPException(status_code=503, detail="PostgreSQL unavailable") from error
    redis_url = os.getenv("WORKSHOP_REDIS_URL", "").strip()
    if redis_url:
        try:
            import redis
            redis.Redis.from_url(redis_url, socket_connect_timeout=1, socket_timeout=1).ping()
        except Exception as error:
            raise HTTPException(status_code=503, detail="Redis unavailable") from error
    return {
        "status": "ready",
        "postgresql": "ready" if store else "not configured",
        "redis": "ready" if redis_url else "not configured",
    }


def _require_api_token(presented: str | None) -> None:
    expected = os.getenv("WORKSHOP_API_TOKEN", "")
    if not expected or not presented or not hmac.compare_digest(expected, presented):
        raise HTTPException(status_code=403, detail="Workshop API token required")


@api.post("/decisions", response_model=DecisionResponse)
def decide(request: DecisionRequest, x_workshop_api_token: str | None = Header(default=None)) -> DecisionResponse:
    _require_api_token(x_workshop_api_token)
    try:
        flow, output = run_assistant(
            question=request.question, customer_id=request.customer_id,
            remember=request.remember, request_email=request.request_email,
            approved=False,  # A public request can never grant its own approval.
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    report = flow.state.report if not flow.state.failure else None
    status = "pending_approval" if request.request_email and report and not flow.state.failure else "complete"
    store = configured_store()
    if store:
        try:
            store.save_run(
                run_id=flow.state.id, customer_id=request.customer_id,
                question=request.question, requested_action=request.request_email,
                report=report if not flow.state.failure else None, output=output,
            )
        except Exception as error:
            raise HTTPException(status_code=503, detail="PostgreSQL write failed") from error
    return DecisionResponse(run_id=flow.state.id, status=status, report=report, output=output)


@api.post("/decisions/{run_id}/approve")
def approve(run_id: UUID, x_workshop_approval_token: str | None = Header(default=None)) -> dict[str, str]:
    expected = os.getenv("WORKSHOP_APPROVAL_TOKEN", "")
    if not expected or not x_workshop_approval_token or not hmac.compare_digest(expected, x_workshop_approval_token):
        raise HTTPException(status_code=403, detail="Instructor approval token required")
    store = configured_store()
    if store is None:
        raise HTTPException(status_code=503, detail="PostgreSQL is required for durable approvals")
    try:
        result = store.approve_mock_action(str(run_id), approved_by="workshop-instructor")
    except KeyError as error:
        raise HTTPException(status_code=404, detail="Run not found") from error
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=503, detail="PostgreSQL approval failed") from error
    return {"run_id": str(run_id), "result": result}
