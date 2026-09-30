# %% [markdown]
# # 07 — One agent becomes a Crew
# The Researcher finds evidence, the Analyst weighs it, and the Critic checks
# the conclusion. A sequential process passes task context along the chain.

# %%
import sys
from pathlib import Path

here = Path(__file__).resolve() if "__file__" in globals() else Path.cwd() / "lesson.py"
sys.path.insert(0, str(next(p for p in here.parents if (p / "pyproject.toml").exists())))

import workshop  # configure project-local CrewAI storage
from crewai import Agent, Crew, Process, Task

from workshop.common import model
from workshop.knowledge import sample_knowledge
from workshop.schemas import DecisionReport
from workshop.tools import company_search_tool, research_tool, roi_tool

llm = model()
researcher = Agent(
    role="Enterprise AI Researcher",
    goal="Gather source-backed facts about the proposed technology",
    backstory="You distinguish evidence from assumptions.",
    llm=llm,
    tools=[company_search_tool, research_tool],
    max_iter=4,
    allow_delegation=False,
)
analyst = Agent(
    role="Enterprise AI Analyst",
    goal="Weigh benefits, costs, constraints, and unknowns",
    backstory="You make conditional, auditable recommendations.",
    llm=llm,
    tools=[roi_tool],
    max_iter=4,
    allow_delegation=False,
)
critic = Agent(
    role="Evidence Critic",
    goal="Find unsupported claims and decide what must be verified",
    backstory="You accept only claims supported by named sources.",
    llm=llm,
    max_iter=4,
    allow_delegation=False,
)

# %% [markdown]
# ## Give every specialist a distinct task
# `context` makes the handoff explicit. The final task asks CrewAI to parse a
# DecisionReport, but the surrounding harness still validates its source IDs.

# %%
research = Task(
    description="Research {question}. Customer constraint: {customer_context}. "
    "Use tools and name the source IDs for every factual claim.",
    expected_output="Evidence notes with source IDs and explicit unknowns.",
    agent=researcher,
)
analysis = Task(
    description="Analyze the research for {question}; label ROI as a scenario.",
    expected_output="Conditional recommendation with tradeoffs and unknowns.",
    agent=analyst,
    context=[research],
)
critique = Task(
    description="Review the analysis and produce a structured final decision. "
    "Cite only architecture.md, security.md, or pricing.md in evidence.",
    expected_output="DecisionReport with recommendation, rationale, evidence, risks, next_steps.",
    agent=critic,
    context=[research, analysis],
    output_pydantic=DecisionReport,
    guardrail_max_retries=1,
)
sources, embedder = sample_knowledge()
crew = Crew(
    agents=[researcher, analyst, critic],
    tasks=[research, analysis, critique],
    process=Process.sequential,
    knowledge_sources=sources,
    embedder=embedder,
)
print("Roles:", [agent.role for agent in crew.agents])
print("Tasks:", [task.description[:55] for task in crew.tasks])

# %% [markdown]
# ## Run and inspect the structured output
# Ask whether the extra roles improved the evidence and critique enough to
# justify their extra model calls and latency.

# %%
result = crew.kickoff(inputs={
    "question": "Should Northstar AI pilot Meridian AI?",
    "customer_context": "Customer A requires private VPC deployment.",
})
print(result.pydantic or result.raw)

# %% [markdown]
# ## Bonus scenario — a two-person content team
# Fewer roles can be enough (inspired by CrewAI's *Content Creator* flow).
# Compare this two-agent Crew with the three-agent Crew above.
# It is shorter than the run above, but still two model tasks on a local model.

# %%
writer = Agent(role="Writer", goal="Draft a short post", backstory="You write plainly.", llm=llm, allow_delegation=False)
editor = Agent(role="Editor", goal="Cut the draft to 60 words", backstory="You remove filler.", llm=llm, allow_delegation=False)
draft = Task(description="Draft a post on why AI agents need tests.", expected_output="A short draft.", agent=writer)
edit = Task(
    description="Edit the draft to at most 60 words.",
    expected_output="The final post.",
    agent=editor,
    context=[draft],
)
print(Crew(agents=[writer, editor], tasks=[draft, edit], process=Process.sequential).kickoff().raw)
