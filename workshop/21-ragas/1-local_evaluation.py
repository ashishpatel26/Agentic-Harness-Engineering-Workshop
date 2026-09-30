# %% [markdown]
# # 21 — Deterministic checks first, Ragas as a second signal
# Ragas judges factual overlap with a local Ollama model. It cannot prove that
# an approval gate or a customer scope was enforced.

# %%
import asyncio
import os
import sys
from pathlib import Path

here = Path(__file__).resolve() if "__file__" in globals() else Path.cwd() / "lesson.py"
sys.path.insert(0, str(next(p for p in here.parents if (p / "pyproject.toml").exists())))

from workshop.control import validate_report
from workshop.ragas_eval import factual_score, load_cases
from workshop.schemas import DecisionReport, Evidence

report = DecisionReport(
    recommendation="pilot",
    rationale="A limited pilot is justified while deletion guarantees remain unverified.",
    evidence=[Evidence(source_id="architecture.md", claim="Private VPC deployment is possible."),
              Evidence(source_id="security.md", claim="Deletion guarantees are unverified.")],
)
print("Deterministic report check:", validate_report(report))
cases = load_cases()
print("Versioned evaluation cases:", [case["id"] for case in cases])

# %% [markdown]
# ## Run a local model-judged score only when requested
# Scores may vary by model and run; record the model and input dataset.

# %%
if os.getenv("WORKSHOP_RUN_LIVE_DEMOS") == "true":
    for case in cases:
        print(case["id"], asyncio.run(factual_score(case["response"], case["reference"])))
else:
    print("Set WORKSHOP_RUN_LIVE_DEMOS=true for the Ragas/Ollama metric.")
