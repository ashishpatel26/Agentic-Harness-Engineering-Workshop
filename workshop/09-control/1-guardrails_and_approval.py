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
