# %% [markdown]
# # 03 — Typed tools and tool choice
# A tool is a bounded Python capability the model can request. First test the
# plain function, then watch the CrewAI agent decide when to use its wrapper.

# %%
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

import workshop  # configure project-local CrewAI storage
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool

from workshop.common import model
from workshop.tools import calculate_annual_roi

print("Pure function:", calculate_annual_roi(45_000, 30_000))
try:
    calculate_annual_roi(45_000, 0)
except ValueError as error:
    print("Input contract:", error)

# %% [markdown]
# ## Wrap the tested function as a CrewAI tool
# The docstring describes when the agent should use this capability. The
# function still validates inputs in Python, independent of model behavior.

# %%
@tool("Calculate annual ROI")
def roi_tool(annual_benefit: float, annual_cost: float) -> str:
    """Calculate a hypothetical annual ROI percentage from stated USD assumptions."""
    value = calculate_annual_roi(annual_benefit, annual_cost)
    return json.dumps({"roi_percent": value, "status": "scenario, not a guarantee"})


print("Available tool:", roi_tool.name)

# %% [markdown]
# ## Give only the required tool to the agent
# The calculation is a scenario, not a measured financial outcome.

# %%
analyst = Agent(
    role="ROI Analyst",
    goal="Calculate transparent planning scenarios",
    backstory="You label estimates and assumptions.",
    llm=model(),
    tools=[roi_tool],
    max_iter=3,
    allow_delegation=False,
    verbose=True,
)
task = Task(
    description="Use the ROI tool for $45,000 annual benefit and $30,000 "
    "annual cost. Explain why the result is only a planning scenario.",
    expected_output="ROI percentage and assumption caveat.",
    agent=analyst,
)
print(Crew(agents=[analyst], tasks=[task], process=Process.sequential).kickoff().raw)

# %% [markdown]
# ## Bonus scenario — a job posting
# A second tool for a different job (inspired by CrewAI's *Job Posting* example).
# The tool rejects an unknown level, and the agent sees that error as an observation.

# %%
@tool("Salary band lookup")
def salary_band(level: str) -> str:
    """Return the fictional Northstar salary band in USD for a level: junior, mid, or senior."""
    bands = {"junior": "60k-80k", "mid": "80k-110k", "senior": "110k-150k"}
    if level.lower() not in bands:
        raise ValueError(f"unknown level '{level}'; use junior, mid, or senior")
    return json.dumps({"level": level.lower(), "band_usd": bands[level.lower()]})


recruiter = Agent(
    role="Recruiter",
    goal="Write accurate job ads",
    backstory="You never invent pay figures.",
    llm=model(),
    tools=[salary_band],
    max_iter=3,
    allow_delegation=False,
)
ad = Task(
    description="Write a two-sentence job ad for a senior agent engineer. "
    "Look up the salary band with the tool and include it.",
    expected_output="Two sentences that include the band from the tool.",
    agent=recruiter,
)
print(Crew(agents=[recruiter], tasks=[ad], process=Process.sequential).kickoff().raw)
