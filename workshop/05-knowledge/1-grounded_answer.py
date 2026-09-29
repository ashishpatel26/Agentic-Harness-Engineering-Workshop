# %% [markdown]
# # 05 — Ground an answer in company knowledge
# Context is what goes into this run. Knowledge is the document collection
# searched for relevant passages. Source IDs make the answer auditable.

# %%
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

import workshop  # configure project-local CrewAI storage
from crewai import Agent, Crew, Process, Task
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from workshop.common import DATA, embedder_config, model
from workshop.tools import DOCUMENTS, search_documents

print("Transparent search before RAG:", search_documents("private deployment security")[:1])
sources = [
    StringKnowledgeSource(content=f"Source ID: {name}\n{(DATA / name).read_text(encoding='utf-8')}")
    for name in DOCUMENTS
]
embedder = embedder_config()
print("CrewAI Knowledge sources:", len(sources))
print("Embedding provider:", embedder["provider"])

# %% [markdown]
# ## CrewAI Knowledge retrieval
# The embedder is explicit. Changing the chat model alone does not configure
# Knowledge or Memory embeddings.

# %%
researcher = Agent(
    role="Company Knowledge Researcher",
    goal="Answer only from named sample company sources",
    backstory="You cite the source ID for every factual claim.",
    llm=model(),
    max_iter=3,
    allow_delegation=False,
)
task = Task(
    description="What is known and unknown about Meridian AI's security? "
    "Cite source IDs. Say when evidence is missing.",
    expected_output="Short answer with source IDs and unknowns.",
    agent=researcher,
)
crew = Crew(
    agents=[researcher], tasks=[task], process=Process.sequential,
    knowledge_sources=sources, embedder=embedder,
)
print(crew.kickoff().raw)

# %% [markdown]
# ## Bonus scenario — matching a candidate
# Knowledge works on any documents (inspired by CrewAI's *Recruitment* example).
# Here three short fictional profiles replace the company files.
# This run takes about as long as the one above; skip it if time is short.

# %%
profiles = [
    StringKnowledgeSource(content="Candidate Asha: 6 years Python, built two CrewAI agents, no cloud experience."),
    StringKnowledgeSource(content="Candidate Ben: 2 years Java, strong on Kubernetes and deployment."),
    StringKnowledgeSource(content="Candidate Chen: 4 years data science, wrote evaluation suites for LLM apps."),
]
screener = Agent(
    role="Talent Screener",
    goal="Recommend the best-matching candidate using only the profiles",
    backstory="You name the candidate and the evidence.",
    llm=model(),
    max_iter=3,
    allow_delegation=False,
)
match = Task(
    description="Who best fits an 'agent engineer who writes Python' role? Name one candidate and why.",
    expected_output="One candidate name and the profile fact that supports it.",
    agent=screener,
)
print(Crew(
    agents=[screener], tasks=[match], process=Process.sequential,
    knowledge_sources=profiles, embedder=embedder,
).kickoff().raw)
