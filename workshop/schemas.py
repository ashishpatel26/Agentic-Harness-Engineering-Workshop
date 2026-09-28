"""Stable contracts shared by the lessons and the final Flow."""

from typing import Literal

from pydantic import BaseModel, Field


class Evidence(BaseModel):
    source_id: str = Field(description="One of architecture.md, security.md, pricing.md")
    claim: str = Field(description="A claim supported by that source")


class DecisionReport(BaseModel):
    recommendation: Literal["adopt", "pilot", "reject", "insufficient"]
    rationale: str
    evidence: list[Evidence] = Field(min_length=1)
    risks: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
