# %% [markdown]
# # 08 — A Flow controls the Crew
# The Crew researches. The Flow validates input, tracks state, limits retries,
# and routes either to a report or an explicit evidence gap.

# %%
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

from workshop.decision_flow import DecisionFlow

flow = DecisionFlow()
output = flow.kickoff(inputs={
    "question": "Should Northstar AI pilot Meridian AI?",
    "customer_id": "customer-a",
    "customer_context": "Customer A requires private VPC deployment.",
})

# %% [markdown]
# ## Inspect the path, not only the answer
# retry_count is capped. An evidence failure is a valid controlled result.

# %%
print("Flow output:", output)
print("Retry count:", flow.state.retry_count)
print("Failure:", flow.state.failure or "none")
print("Report:", flow.state.report)
