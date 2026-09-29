# %% [markdown]
# # 20 — Opt-in Langfuse traces
# The core workshop's local JSONL trace stays available without a server.
# External traces can include prompts, so enable them only for approved data.

# %%
import os
import sys
from pathlib import Path

here = Path(__file__).resolve() if "__file__" in globals() else Path.cwd() / "lesson.py"
sys.path.insert(0, str(next(p for p in here.parents if (p / "pyproject.toml").exists())))

from workshop.langfuse_tracing import enable_langfuse
from workshop.common import ensure_runtime

print("Local trace:", ensure_runtime() / "trace.jsonl")
print("Langfuse enabled:", os.getenv("WORKSHOP_LANGFUSE_ENABLED", "false"))

# %% [markdown]
# ## Connect to Langfuse only with explicit permission and project keys
# The integration instruments CrewAI calls made after it is enabled.

# %%
if os.getenv("WORKSHOP_RUN_LIVE_DEMOS") == "true":
    print("Remote instrumentation active:", enable_langfuse())
else:
    print("Set WORKSHOP_RUN_LIVE_DEMOS=true to verify the configured Langfuse project.")
