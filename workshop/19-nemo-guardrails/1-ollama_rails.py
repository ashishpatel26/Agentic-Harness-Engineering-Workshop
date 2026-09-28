# %% [markdown]
# # 19 — NeMo Guardrails with the same Ollama model
# Input and output self-check rails are advisory safety screens. Pydantic,
# citation checks, and server-side approval remain the hard boundaries.

# %%
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

from workshop.nemo_guardrails import check_input, check_output, enabled

print("NeMo enabled:", enabled())
print("Configured model:", os.getenv("WORKSHOP_MODEL", "ollama/qwen3.5:4b"))

# %% [markdown]
# ## Run a local-model check when NeMo is enabled
# This is opt-in because the self-check invokes the local model twice.

# %%
if os.getenv("WORKSHOP_RUN_LIVE_DEMOS") == "true":
    if not enabled():
        raise RuntimeError("Set WORKSHOP_NEMO_ENABLED=true for the live guardrail lab")
    question = "Should Northstar AI pilot Meridian AI?"
    check_input(question)
    check_output(question, '{"recommendation":"pilot","rationale":"verify security claims"}')
    print("Input and output rails passed")
else:
    print("Enable NeMo and WORKSHOP_RUN_LIVE_DEMOS=true for model-backed checks.")
