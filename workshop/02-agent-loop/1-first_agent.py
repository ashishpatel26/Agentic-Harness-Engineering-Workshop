# %% [markdown]
# # 02 — The agent loop
# A model call returns text. An agent can choose a tool, inspect its result,
# and continue. This tiny Python loop makes that mechanism visible first.

# %%
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

import workshop  # configure project-local CrewAI storage
from crewai import Agent, Crew, Process, Task

from workshop.common import model
from workshop.tools import calculate_annual_roi

# A deterministic stand-in for the model's action decision. It lets us see the
# loop before CrewAI and the model take over the decision in the next cell.
state: dict[str, float | None] = {"roi": None}
for step in range(3):
    if state["roi"] is None:
        print(f"Step {step + 1}: choose calculate_annual_roi")
        state["roi"] = calculate_annual_roi(45_000, 30_000)
        print(f"Observation: {state['roi']}% scenario ROI")
    else:
        print(f"Step {step + 1}: answer using observation, with a caveat")
        break

# %% [markdown]
# ## A bounded CrewAI agent
# CrewAI now manages the model/tool loop. The role, task, and limits are explicit.
# There is one agent and one task, so this is the smallest useful CrewAI run.

# %%
researcher = Agent(
    role="Enterprise AI Researcher",
    goal="Explain an adoption question without pretending unknowns are facts",
    backstory="You are cautious about weak evidence.",
    llm=model(),
    max_iter=3,
    max_execution_time=90,
    allow_delegation=False,
)
task = Task(
    description="Should Northstar pilot Meridian AI? We estimate $45k annual benefit "
    "and $30k cost, but have not verified data deletion or throughput.",
    expected_output="A short conditional recommendation and two unknowns.",
    agent=researcher,
)
result = Crew(agents=[researcher], tasks=[task], process=Process.sequential).kickoff()
print(result.raw)

# %% [markdown]
# ## Bonus scenario — a surprise trip
# One agent, one task, explicit limits (inspired by CrewAI's *Surprise Trip* example).
# Check the answer against the budget yourself: the agent may not add correctly.

# %%
planner = Agent(
    role="Surprise Trip Planner",
    goal="Plan a one-day outing that fits the budget",
    backstory="You love small, memorable adventures.",
    llm=model(),
    max_iter=3,
    max_execution_time=240,
    allow_delegation=False,
)
trip = Task(
    description="Plan a one-day surprise outing in Pune for two friends who like "
    "food and hills. Total budget: 2,000 INR. Give a 2-stop itinerary.",
    expected_output="A 2-stop itinerary with a rough cost for each stop.",
    agent=planner,
)
print(Crew(agents=[planner], tasks=[trip], process=Process.sequential).kickoff().raw)
