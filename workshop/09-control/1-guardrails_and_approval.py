# %% [markdown]
# # 09 — Guardrails and human approval
# Validate before the Crew runs. Check the report before accepting it. A mock
# email is a side effect, so it requires approval immediately before execution.

# %%
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

from workshop.control import mock_email, validate_question, validate_report
from workshop.schemas import DecisionReport, Evidence

try:
    validate_question("hi")
except ValueError as error:
    print("Input blocked:", error)

report = DecisionReport(
    recommendation="pilot",
    rationale="A private deployment is possible, but deletion and throughput need verification.",
    evidence=[
        Evidence(source_id="architecture.md", claim="Private VPC deployment is possible."),
        Evidence(source_id="security.md", claim="Data deletion guarantees are unverified."),
    ],
    risks=["Unverified deletion guarantees"],
    next_steps=["Run a bounded pilot"],
)
print("Output check:", validate_report(report))

# %% [markdown]
# ## Exercise the approval boundary
# First run is denied. Second run records a local mock action. A repeated
# action ID is ignored, which matters when an interrupted Flow resumes.

# %%
print(mock_email(report, approved=False, action_id="lesson-09-demo"))
print(mock_email(report, approved=True, action_id="lesson-09-demo"))
print(mock_email(report, approved=True, action_id="lesson-09-demo"))

# %% [markdown]
# ## Bonus scenario — an email auto-responder
# A task guardrail checks a draft before it is accepted (inspired by CrewAI's
# *Email Auto Responder* flow). Test the check on plain text first.

# %%
from crewai import Agent, Crew, Process, Task, TaskOutput

from workshop.common import model


def no_promises(output: TaskOutput) -> tuple[bool, str]:
    if "guarantee" in output.raw.lower():
        return False, "Do not promise guarantees; offer to look into it instead."
    return True, output.raw


print(no_promises(TaskOutput(description="d", raw="We guarantee a refund.", agent="a")))
print(no_promises(TaskOutput(description="d", raw="We will look into your order.", agent="a")))

support = Agent(role="Support Agent", goal="Reply politely", backstory="You never over-promise.", llm=model(), allow_delegation=False)
reply = Task(
    description="Reply in two sentences to a customer whose parcel is late.",
    expected_output="A polite two-sentence reply.",
    agent=support,
    guardrail=no_promises,
    guardrail_max_retries=1,
)
print(Crew(agents=[support], tasks=[reply], process=Process.sequential).kickoff().raw)
