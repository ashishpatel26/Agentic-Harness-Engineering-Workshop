# %% [markdown]
# # 14 — Diagnose the broken harness
# Eight small faults represent capability, context, memory, intelligence,
# orchestration, control, and verification. Pair up: fix one or two faults,
# run the checks again, then compare diagnoses with the room.

# %%
import sys
from pathlib import Path

here = Path(__file__).resolve() if "__file__" in globals() else Path.cwd() / "lesson.py"
sys.path.insert(0, str(next(p for p in here.parents if (p / "pyproject.toml").exists())))

from workshop.control import validate_report
from workshop.schemas import DecisionReport, Evidence
from workshop.tools import calculate_annual_roi


def choose_tool(question: str) -> str:
    """Fault 1: ROI questions should use the calculator."""
    return "Search company documents"  # BUG


def bad_roi(benefit: float, cost: float) -> float:
    """Fault 2: invalid cost should not produce an answer."""
    return 0.0 if cost == 0 else calculate_annual_roi(benefit, cost)  # BUG


def cited_report() -> DecisionReport:
    """Fault 3: one source ID is not in the sample corpus."""
    return DecisionReport(
        recommendation="pilot",
        rationale="A pilot may be justified if missing security evidence is gathered first.",
        evidence=[
            Evidence(source_id="architecture.md", claim="Private deployment is possible."),
            Evidence(source_id="vendor-blog.md", claim="Deletion is guaranteed."),  # BUG
        ],
    )


def memory_scope(customer_id: str) -> str:
    """Fault 4: all customers are mapped to the same scope."""
    return "/customer/shared"  # BUG


def conclusion(report: DecisionReport) -> str:
    """Fault 5: full adoption is asserted despite unresolved evidence."""
    return "adopt"  # BUG


def research_attempts(max_retry: int) -> int:
    """Fault 6: the configured retry cap is ignored."""
    return max_retry + 5  # BUG


def may_send_email(approved: bool) -> bool:
    """Fault 7: a side effect can happen without approval."""
    return True  # BUG


def trace_events() -> list[str]:
    """Fault 8: tool use is missing from the trace."""
    return ["CrewKickoffStartedEvent", "CrewKickoffCompletedEvent"]  # BUG


def rejects_invalid_cost() -> bool:
    try:
        bad_roi(45_000, 0)
    except ValueError:
        return True
    return False


# %% [markdown]
# ## Run the failure checks
# A failing check is the clue, not the solution. Use the function, its boundary,
# and what the earlier labs taught to make the smallest justified repair.

# %%
checks = {
    "1 tool choice": choose_tool("Calculate annual ROI") == "Calculate annual ROI",
    "2 input contract": rejects_invalid_cost(),
    "3 source validation": validate_report(cited_report())[0],
    "4 memory isolation": memory_scope("A") != memory_scope("B"),
    "5 supported conclusion": conclusion(cited_report()) != "adopt",
    "6 bounded retries": research_attempts(1) <= 2,
    "7 approval boundary": not may_send_email(False),
    "8 tool trace": "ToolUsageFinishedEvent" in trace_events(),
}
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL"), name)
