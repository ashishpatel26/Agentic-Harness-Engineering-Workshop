# %% [markdown]
# # 04 — A tool delivered through MCP
# MCP changes how the tool is connected. CrewAI still gives the agent a tool.
# The local server exposes only a read-only annual ROI calculation.

# %%
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()
sys.path.insert(0, str(ROOT))

import workshop  # configure project-local CrewAI storage
from crewai import Agent, Crew, Process, Task
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters

from workshop.common import model

server = StdioServerParameters(
    command=sys.executable,
    args=[str(ROOT / "workshop" / "mcp_server.py")],
)

# %% [markdown]
# ## Connect, inspect, and use the remote tool
# The context manager starts and stops the stdio server. Never put a normal
# print statement on the server's stdout; that channel carries MCP messages.

# %%
with MCPServerAdapter(server) as tools:
    print("MCP tools:", [item.name for item in tools])
    analyst = Agent(
        role="ROI Analyst",
        goal="Calculate a planning scenario through MCP",
        backstory="You distinguish estimates from measured outcomes.",
        llm=model(),
        tools=tools,
        max_iter=3,
        allow_delegation=False,
    )
    task = Task(
        description="Use the MCP annual_roi tool with benefit 45000 and cost 30000.",
        expected_output="Scenario ROI percentage with a caveat.",
        agent=analyst,
    )
    print(Crew(agents=[analyst], tasks=[task], process=Process.sequential).kickoff().raw)
