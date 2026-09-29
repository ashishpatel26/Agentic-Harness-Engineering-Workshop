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

# %% [markdown]
# ## Bonus scenario — a cost meter for a tiny game designer
# Write your own listener in a few lines (inspired by CrewAI's *Game Builder* crew).
# Counting model calls is the simplest cost signal.

# %%
from crewai import Agent, Crew, Process, Task
from crewai.events import BaseEventListener, LLMCallCompletedEvent

from workshop.common import model


class CallCounter(BaseEventListener):
    def __init__(self):
        self.llm_calls = 0
        super().__init__()

    def setup_listeners(self, event_bus):
        @event_bus.on(LLMCallCompletedEvent)
        def count(_source, _event):
            self.llm_calls += 1


counter = CallCounter()
designer = Agent(role="Game Designer", goal="Design tiny games", backstory="You keep rules short.", llm=model(), allow_delegation=False)
rules = Task(
    description="Write the rules of a guess-the-number game in three bullets.",
    expected_output="Three bullets.",
    agent=designer,
)
print(Crew(agents=[designer], tasks=[rules], process=Process.sequential).kickoff().raw)
print("Model calls made:", counter.llm_calls)
