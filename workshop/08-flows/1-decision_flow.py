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

# %% [markdown]
# ## Bonus scenario — lead scoring
# A Flow needs no model to route work (inspired by CrewAI's *Lead Score* flow).
# Typed state, a router, and one listener per branch: the same shape as above.

# %%
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel


class LeadState(BaseModel):
    budget_usd: int = 0
    team_size: int = 0
    score: int = 0


class LeadFlow(Flow[LeadState]):
    @start()
    def score_lead(self):
        self.state.score = min(self.state.budget_usd // 1000, 60) + min(self.state.team_size, 40)

    @router(score_lead)
    def route(self):
        return "hot" if self.state.score >= 70 else "nurture"

    @listen("hot")
    def call_today(self):
        return f"Score {self.state.score}: call today"

    @listen("nurture")
    def send_newsletter(self):
        return f"Score {self.state.score}: add to newsletter"


print(LeadFlow().kickoff(inputs={"budget_usd": 50_000, "team_size": 30}))
print(LeadFlow().kickoff(inputs={"budget_usd": 5_000, "team_size": 4}))
