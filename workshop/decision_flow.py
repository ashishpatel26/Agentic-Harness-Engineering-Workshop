"""The final CrewAI Flow: control and state around the research Crew."""

from __future__ import annotations

from uuid import uuid4

from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel, Field

from workshop.control import mock_email, validate_question, validate_report
from workshop.crew import build_research_crew
from workshop.nemo_guardrails import check_output
from workshop.schemas import DecisionReport


class DecisionState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    question: str = ""
    customer_id: str = "demo"
    customer_context: str = "No saved customer constraint."
    request_email: bool = False
    approved: bool = False
    retry_count: int = 0
    report: DecisionReport | None = None
    failure: str = ""
    action_result: str = ""


class DecisionFlow(Flow[DecisionState]):
    """The Flow decides *when* work happens; the Crew decides *how* to research."""

    @start()
    def validate_request(self) -> str:
        self.state.question = validate_question(self.state.question)
        return self.state.question

    @listen(validate_request)
    def research(self, question: str) -> bool:
        for attempt in range(2):
            result = build_research_crew().kickoff(inputs={
                "question": question,
                "customer_context": self.state.customer_context,
            })
            report = result.pydantic
            if report is None:
                self.state.failure = "Crew did not return a structured report"
            else:
                self.state.report = DecisionReport.model_validate(report)
                valid, reason = validate_report(self.state.report)
                if valid:
                    try:
                        check_output(question, self.state.report.model_dump_json())
                    except ValueError as error:
                        self.state.failure = str(error)
                    else:
                        self.state.failure = ""
                        return True
                    self.state.retry_count = attempt + 1
                    continue
                self.state.failure = reason
            self.state.retry_count = attempt + 1
        return False

    @router(research)
    def route_result(self, valid: bool) -> str:
        if not valid:
            return "insufficient"
        if self.state.request_email:
            return "approved_action" if self.state.approved else "pending_approval"
        return "report_ready"

    @listen("report_ready")
    def finish_report(self) -> str:
        assert self.state.report is not None
        return self.state.report.model_dump_json(indent=2)

    @listen("pending_approval")
    def wait_for_approval(self) -> str:
        return "PENDING_APPROVAL: report ready; mock email was not executed"

    @listen("approved_action")
    def execute_approved_action(self) -> str:
        assert self.state.report is not None
        self.state.action_result = mock_email(
            self.state.report,
            approved=self.state.approved,
            action_id=self.state.id,
        )
        return self.state.action_result

    @listen("insufficient")
    def report_gap(self) -> str:
        return f"INSUFFICIENT_EVIDENCE: {self.state.failure}"
