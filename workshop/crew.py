"""A focused Researcher → Analyst → Critic Crew."""

import os

from crewai import Agent, Crew, Process, Task

from workshop.common import model
from workshop.knowledge import sample_knowledge
from workshop.schemas import DecisionReport
from workshop.tools import company_search_tool, research_tool, roi_tool


def build_research_crew(*, with_knowledge: bool = True) -> Crew:
    llm = model()
    sources, embedder = sample_knowledge()
    researcher_tools = [company_search_tool, research_tool]
    if os.getenv("WORKSHOP_LANCEDB_RAG_ENABLED", "false").lower() == "true":
        from workshop.retrieval import index_documents, lancedb_search_tool

        index_documents()
        researcher_tools.append(lancedb_search_tool)
    researcher = Agent(
        role="Enterprise AI Researcher",
        goal="Gather source-backed facts about the proposed technology",
        backstory="You distinguish evidence from assumptions.",
        llm=llm,
        tools=researcher_tools,
        max_iter=4,
        max_execution_time=120,
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
    research = Task(
        description="Research {question}. Customer constraint: {customer_context}. "
        "Use tools and name the source IDs for every factual claim.",
        expected_output="Brief evidence notes with source IDs and explicit unknowns.",
        agent=researcher,
    )
    analysis = Task(
        description="Analyze the research for {question}; label ROI as a scenario.",
        expected_output="A conditional recommendation with tradeoffs and unknowns.",
        agent=analyst,
        context=[research],
    )
    critique = Task(
        description="Review the analysis and produce a structured final decision. "
        "Cite only architecture.md, security.md, or pricing.md in evidence. "
        "Unknowns must appear in risks or next_steps.",
        expected_output="DecisionReport with recommendation, rationale, evidence, risks, next_steps.",
        agent=critic,
        context=[research, analysis],
        output_pydantic=DecisionReport,
        guardrail_max_retries=1,
    )
    return Crew(
        agents=[researcher, analyst, critic],
        tasks=[research, analysis, critique],
        process=Process.sequential,
        knowledge_sources=sources if with_knowledge else None,
        embedder=embedder if with_knowledge else None,
        verbose=False,
    )
