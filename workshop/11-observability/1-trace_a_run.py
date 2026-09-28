# %% [markdown]
# # 11 — Trace a run
# CrewAI emits execution events. This local listener records event types and
# times without capturing prompts or document contents. CrewAI's full tracing
# integration can be enabled separately when the organization approves it.

# %%
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

from workshop.common import ensure_runtime
from workshop.crew import build_research_crew
from workshop.observability import LocalTrace

listener = LocalTrace()
result = build_research_crew().kickoff(inputs={
    "question": "Should Northstar AI pilot Meridian AI?",
    "customer_context": "No saved customer constraint.",
})

# %% [markdown]
# ## Read the local trace
# Find the Crew start/end, model calls, and tool events. Compare the event
# sequence with the report to diagnose a missing tool or unexpected retry.

# %%
print(result.raw)
print((ensure_runtime() / "trace.jsonl").read_text(encoding="utf-8")[-3000:])
