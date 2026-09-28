# %% [markdown]
# # 01 — From a Python function to a model call
# Problem: fixed rules cannot synthesize an answer when evidence is incomplete.
# Watch what changes when the program calls a model: the output becomes useful,
# but the model may assert something that the input never established.

# %%
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

from workshop.common import model


def fixed_recommendation(annual_benefit: int, annual_cost: int) -> str:
    return "pilot" if annual_benefit > annual_cost else "investigate further"


print("Python rule:", fixed_recommendation(45_000, 30_000))

# %% [markdown]
# ## The first model call
# CrewAI's LLM object supplies the model here. The input deliberately omits
# security evidence. Compare the model response with the facts provided.

# %%
response = model().call(
    "A fictional AI platform may save $45,000/year and cost $30,000/year. "
    "We have not verified data deletion or throughput. Recommend adopt, pilot, "
    "or reject in two sentences. State what is still unknown."
)
print("Model response:", response)
