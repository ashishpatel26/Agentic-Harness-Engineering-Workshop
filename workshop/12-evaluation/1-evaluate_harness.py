# %% [markdown]
# # 12 — Evaluate behavior, not just prose
# Objective checks should be plain Python. A model-judged score can be added
# later, but approval, citation IDs, and bounded retries must be testable code.

# %%
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

from workshop.control import mock_email, validate_report
from workshop.schemas import DecisionReport, Evidence
from workshop.tools import calculate_annual_roi

cases = [
    ("roi scenario", lambda: calculate_annual_roi(45_000, 30_000) == 50.0),
    ("zero cost rejected", lambda: rejects_zero_cost()),
    ("email blocked", lambda: mock_email(example_report, approved=False, action_id="eval-denied").startswith("BLOCKED")),
    ("citations valid", lambda: validate_report(example_report)[0]),
]


def rejects_zero_cost() -> bool:
    try:
        calculate_annual_roi(45_000, 0)
    except ValueError:
        return True
    return False


example_report = DecisionReport(
    recommendation="pilot",
    rationale="The possible benefit merits a pilot, while security gaps block full adoption.",
    evidence=[
        Evidence(source_id="pricing.md", claim="Annual benefit is estimated at $45,000."),
        Evidence(source_id="security.md", claim="Deletion guarantees are unverified."),
    ],
)

# %% [markdown]
# ## Run the checks
# Extend the set with a model run after establishing this deterministic base.

# %%
for name, check in cases:
    print(("PASS" if check() else "FAIL"), name)
