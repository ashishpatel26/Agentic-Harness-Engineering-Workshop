
Yes. With **CrewAI**, I would change the workshop design substantially.

I reviewed the versioned CrewAI documentation you linked, including the core architecture, Agents, Tasks, Crews, Flows, Knowledge, Memory, Reasoning, Planning, Testing, Checkpointing, Streaming, MCP, HITL, Tools, Processes, Collaboration, and production-architecture sections. The strongest architectural message in this version is **Flow-first: Flow provides control/state/orchestration, while Crew provides autonomous intelligence inside the Flow**. ([CrewAI Documentation][1])

That maps extremely well to an **Agentic Harness** workshop.

# Recommended workshop

# **Engineering an Agentic Harness with CrewAI**

### **From Autonomous Agents → Controlled Crews → Stateful Flows → Observable Production Systems**

**9:00 AM – 5:00 PM | 100% hands-on / architecture-driven**

The workshop should **not** be “Learn CrewAI.”

The learning objective should be:

> **Build a production-style Agentic Harness that gives AI agents capabilities, context, memory, control, orchestration, safety, observability and evaluation.**

CrewAI is the implementation framework.

---

# 1. The mental model I recommend

Use this throughout the workshop:

## **Agent = Employee**

## **Crew = Team**

## **Flow = Manager / Business Process**

## **Harness = Company Operating System**

```text
                         BUSINESS GOAL
                              │
                              ▼
                    ┌───────────────────┐
                    │   AGENTIC HARNESS │
                    │                   │
                    │   FLOW            │
                    │   ┌────────────┐  │
                    │   │   CREW     │  │
                    │   │            │  │
                    │   │ Researcher │  │
                    │   │ Analyst    │  │
                    │   │ Critic     │  │
                    │   └────────────┘  │
                    │                   │
                    │ Knowledge         │
                    │ Memory            │
                    │ Tools / MCP       │
                    │ Guardrails        │
                    │ HITL              │
                    │ Checkpoints       │
                    │ Observability     │
                    │ Evaluation        │
                    └─────────┬─────────┘
                              │
                              ▼
                       TRUSTED RESULT
```

This isn't just a metaphor. CrewAI's own architecture now describes **Flows as the backbone/scaffolding** and **Crews as the autonomous units of work inside them**. Its production guidance explicitly recommends starting with a Flow for robust applications. ([CrewAI Documentation][1])

---

# 2. The six-layer Agentic Harness

I would make this the central architecture of the workshop.

```text
                  AGENTIC HARNESS
                         │
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
  1. CONTROL                         6. ORCHESTRATE
  What may happen?                  How does work flow?
        │                                 │
        ▼                                 ▼
  Guardrails                         Flow
  HITL                               Crew
  Permissions                       Tasks
  Policies                           Processes
        │                                 │
        ├───────────────┬─────────────────┤
        ▼               ▼                 ▼
  2. CAPABILITY     3. CONTEXT       4. MEMORY
  What can it do?   What does it     What should it
                    know now?        remember?
        │               │                 │
      Tools            RAG              Memory
      MCP              Knowledge        State
      APIs             Files             Sessions
        │               │                 │
        └───────────────┼─────────────────┘
                        ▼
                  5. INTELLIGENCE
                        │
                    Agents
                    Reasoning
                    Planning
                    Delegation
                        │
                        ▼
                  7. VERIFY
                        │
                Observability
                Evaluation
                Testing
                Checkpointing
```

I'd actually call it **7 layers**, because verification deserves its own layer.

---

# 3. The single project for the entire day

Don't build isolated demos.

Build one system incrementally:

# **Enterprise AI Research & Decision Harness**

User asks:

> "Should our company adopt technology X for enterprise AI?"

The system must:

1. validate the request
2. retrieve internal knowledge
3. research external information
4. use tools
5. delegate research to specialized agents
6. analyze findings
7. critique the answer
8. request human approval where required
9. maintain state/memory
10. produce a structured report
11. expose execution traces
12. evaluate the final result

Architecture:

```text
User
 │
 ▼
FastAPI / Streamlit
 │
 ▼
┌────────────────────────────────────────────┐
│             AGENTIC HARNESS                │
│                                            │
│                 CrewAI Flow                │
│                      │                     │
│              ┌───────▼────────┐            │
│              │   Research Crew │            │
│              │                 │            │
│              │ Researcher     │            │
│              │ Analyst        │            │
│              │ Critic         │            │
│              └───────┬────────┘            │
│                      │                     │
│        ┌─────────────┼─────────────┐       │
│        ▼             ▼             ▼       │
│      Tools        Knowledge       Memory   │
│      MCP           RAG            State    │
│                                            │
│        Guardrails → HITL → Validation     │
│                                            │
│        Tracing → Metrics → Evaluation     │
└──────────────────────┬─────────────────────┘
                       │
                       ▼
                 Final Report
```

---

# 4. Technology stack

Since you previously wanted a **mostly open-source stack**, I'd use:

| Layer                        | Workshop technology                     |
| ---------------------------- | --------------------------------------- |
| Agent framework              | **CrewAI**                        |
| Workflow                     | **CrewAI Flows**                  |
| LLM                          | **Ollama + local open model**     |
| API                          | **FastAPI**                       |
| UI                           | **Streamlit**                     |
| RAG                          | **CrewAI Knowledge + Qdrant**     |
| Database                     | **PostgreSQL**                    |
| Memory                       | **CrewAI Memory**                 |
| Cache                        | **Redis**                         |
| Tools                        | Python custom tools                     |
| External tools               | **MCP**                           |
| Guardrails                   | CrewAI guardrails + Python/Pydantic     |
| Observability                | **OpenTelemetry + Arize Phoenix** |
| Evaluation                   | **Ragas**                         |
| Testing                      | pytest +`crewai test`                 |
| Deployment                   | Docker / Docker Compose                 |
| Optional auth                | Keycloak                                |
| Optional workflow resilience | CrewAI Checkpointing                    |

CrewAI's Knowledge abstraction supports ChromaDB by default and Qdrant as another supported vector store, so Qdrant is a reasonable open-source choice for the workshop. ([CrewAI Documentation][2])

---

# 5. 9:00–9:30

# Module 1 — What is an Agentic Harness?

Don't start with Python.

Start with:

### LLM

```text
Prompt → LLM → Response
```

### Agent

```text
Goal
 ↓
Reason
 ↓
Tool
 ↓
Observe
 ↓
Act
```

### Agentic system

```text
Agent
 ├── Tools
 ├── Knowledge
 ├── Memory
 ├── Other agents
 └── Workflow
```

### Agentic Harness

```text
Agent
 +
Control
 +
Context
 +
Memory
 +
Orchestration
 +
Observability
 +
Evaluation
```

### Exercise

Give them a deliberately unsafe/unreliable agent and ask:

> **What would you add before allowing this agent into production?**

This creates the need for the harness organically.

---

# 6. 9:30–10:15

# Module 2 — Agent Engineering

Teach:

* Role
* Goal
* Backstory
* LLM
* Tools
* max iterations
* retries
* rate limits
* execution timeout
* reasoning
* memory
* knowledge

CrewAI's Agent API exposes controls such as `max_iter`, `max_rpm`, `max_execution_time`, `max_retry_limit`, `reasoning`, `knowledge_sources`, memory and tool configuration. ([CrewAI Documentation][3])

### Hands-on

Build:

```python
researcher = Agent(
    role="Enterprise AI Researcher",
    goal="Research a technology and identify enterprise implications",
    backstory="You are a senior enterprise technology researcher.",
    tools=[search_tool],
    reasoning=True,
    max_iter=10,
    max_retry_limit=2,
    verbose=True,
)
```

The participants now have their first employee.

---

# 7. 10:15–11:00

# Module 3 — Capability Layer

## Tools → MCP → APIs

Teach the distinction:

```text
Tool
 ↓
Local callable capability

MCP
 ↓
Remote standardized capability

API
 ↓
External service
```

CrewAI currently treats Tools, MCP servers and Apps as action capabilities, while Skills and Knowledge serve different purposes: Skills inject expertise/instructions, and Knowledge provides retrieved information. ([CrewAI Documentation][4])

### Hands-on

Build three tools:

```text
search_company_docs()
search_web()
calculate_roi()
```

Then add an MCP server.

This gives participants the mental model:

> **Tools tell the agent what it can DO.**

---

# 8. 11:00–11:45

# Module 4 — Context + Knowledge + RAG

Build:

```text
PDF / Markdown
      │
      ▼
Knowledge Source
      │
      ▼
Embedding
      │
      ▼
Qdrant
      │
      ▼
Semantic Retrieval
      │
      ▼
Agent
```

CrewAI Knowledge is explicitly designed as the agent's reference library for domain-specific information and grounding, with RAG support through ChromaDB and Qdrant. ([CrewAI Documentation][2])

### Advanced challenge

Give the agent:

```text
architecture.pdf
security.pdf
pricing.pdf
compliance.pdf
```

Ask:

> "Should we deploy this platform?"

Now they must retrieve evidence before answering.

---

# 9. 11:45–12:15

# Module 5 — Memory

This is where your harness gets interesting.

Teach:

```text
Context ≠ Memory
```

### Context

What the agent needs **right now**.

### Memory

What the system should **remember across interactions**.

CrewAI's current Memory API is unified rather than requiring separate short-term/long-term/entity APIs, and it supports storing, recalling and forgetting memories with composite relevance scoring. ([CrewAI Documentation][5])

### Hands-on

```python
memory = Memory()

memory.remember(
    "The customer prefers AWS and requires private deployment."
)

results = memory.recall(
    "What deployment constraints does the customer have?"
)
```

---

# 10. 12:15–1:00

# Module 6 — Crew: From One Agent to a Team

Now introduce:

```text
                  RESEARCH CREW
                       │
              ┌────────┼────────┐
              ▼        ▼        ▼
          Researcher Analyst  Critic
              │        │        │
              └────────┼────────┘
                       ▼
                  Research Result
```

Teach:

* Agent specialization
* Task ownership
* delegation
* sequential process
* hierarchical process
* manager agent

CrewAI supports sequential and hierarchical processes; hierarchical execution uses a manager LLM or custom manager agent to allocate and review work. ([CrewAI Documentation][6])

### Key design question

> **When should I use one agent vs a Crew?**

That is much more valuable than simply showing how to instantiate three agents.

---

# 11. 1:00–2:00

# Lunch

---

# 12. 2:00–2:50

# Module 7 — Flow: The Real Harness

This should be the **most important module of the workshop**.

Because this is where CrewAI becomes an Agentic Harness rather than just a multi-agent framework.

CrewAI recommends the **Flow-first architecture** for production applications because Flows provide state management, control flow, branching, loops and a structured execution boundary. ([CrewAI Documentation][7])

Build:

```text
                         FLOW
                          │
                    ┌─────▼─────┐
                    │ Validate  │
                    └─────┬─────┘
                          ▼
                    ┌───────────┐
                    │ Research  │
                    │   Crew    │
                    └─────┬─────┘
                          ▼
                    ┌───────────┐
                    │ Validate  │
                    └─────┬─────┘
                          │
                   ┌──────┴──────┐
                   ▼             ▼
                 PASS           FAIL
                   │             │
                   ▼             ▼
                Report       Research Again
```

### Code

```python
class ResearchState(BaseModel):
    question: str = ""
    research: str = ""
    report: str = ""
    approved: bool = False


class ResearchFlow(Flow[ResearchState]):

    @start()
    def validate_request(self):
        return self.state.question

    @listen(validate_request)
    def run_research(self, question):
        crew = ResearchCrew()
        result = crew.crew().kickoff(
            inputs={"question": question}
        )

        self.state.research = result.raw
        return result.raw

    @listen(run_research)
    def generate_report(self, research):
        self.state.report = research
        return research
```

This follows the Flow pattern documented by CrewAI: typed state, `@start()`, `@listen()`, and explicit delegation from Flow to Crew. ([CrewAI Documentation][7])

---

# 13. 2:50–3:20

# Module 8 — Reasoning + Planning

Now make the agents smarter.

### Agent reasoning

```text
Task
 ↓
Reflect
 ↓
Plan
 ↓
Evaluate plan
 ↓
Execute
```

CrewAI's reasoning feature allows an agent to create/refine a plan before execution. ([CrewAI Documentation][8])

### Crew planning

```python
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential,
    planning=True
)
```

Planning operates across the Crew's tasks and injects the resulting plan into task descriptions. ([CrewAI Documentation][9])

### Important exercise

Run:

```text
No reasoning
      vs
Reasoning
      vs
Crew planning
```

Compare:

* latency
* number of LLM calls
* quality
* cost
* failure modes

That turns a feature demo into an engineering lesson.

---

# 14. 3:20–3:35

# Break

---

# 15. 3:35–4:05

# Module 9 — Control Layer

Now introduce:

### Guardrails

```text
User
 ↓
Input Guardrail
 ↓
Agent
 ↓
Output Guardrail
 ↓
Response
```

### HITL

```text
Agent
 ↓
Sensitive Action?
 ↓
Human Review
 ├── Approve
 └── Reject
```

CrewAI supports task-level human input and Flow-based human feedback; its documentation also distinguishes local synchronous HITL from webhook-based production approaches. ([CrewAI Documentation][10])

### Exercise

Agent wants to:

> Send an email to a customer.

Harness responds:

```text
⚠ ACTION REQUIRES HUMAN APPROVAL

Approve?
[Y] [N]
```

---

# 16. 4:05–4:30

# Module 10 — Resilience

This is the advanced section that most introductory workshops miss.

Teach:

* retries
* timeout
* rate limits
* cache
* checkpointing
* resume
* failure recovery

CrewAI's checkpointing mechanism saves execution state so a Flow, Crew or Agent can resume after failure, including state, task progress, intermediate outputs and event history. ([CrewAI Documentation][11])

### Failure simulation

Kill the process:

```text
Research
  ↓
Analysis
  ↓
💥 PROCESS CRASH
```

Resume:

```text
Checkpoint
   ↓
Restore state
   ↓
Skip completed work
   ↓
Continue
```

This is a very good **senior-level Agentic Harness exercise**.

---

# 17. 4:30–4:50

# Module 11 — Observability + Testing

Now answer:

> **How do I know what the agent actually did?**

Use:

```text
Flow
 │
 ├── Agent
 │    ├── LLM
 │    ├── Tool
 │    └── Retrieval
 │
 ├── Agent
 │
 └── Output
```

Trace:

* latency
* tool calls
* task execution
* LLM calls
* failures
* token/cost information

CrewAI provides tracing for Crews and Flows, including agent decisions, task timelines, tool usage and LLM calls. ([CrewAI Documentation][12])

Then:

```bash
crewai test -n 5
```

CrewAI's testing command runs the Crew repeatedly and reports performance metrics. ([CrewAI Documentation][13])

---

# 18. 4:50–5:00

# Final Challenge

Give them a broken harness.

```text
❌ Wrong tool selected
❌ Hallucinated answer
❌ Missing context
❌ Agent loops
❌ No human approval
❌ Flow loses state
❌ No trace
❌ Poor evaluation
```

Their task:

> **Diagnose and repair the Agentic Harness.**

They must identify which layer failed:

```text
              FAILURE
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
 Capability   Context     Memory
     │           │           │
     └───────────┼───────────┘
                 ▼
             Intelligence
                 │
                 ▼
              Control
                 │
                 ▼
            Orchestration
                 │
                 ▼
             Verification
```

---

# 19. The final architecture participants build

By 5 PM, their code should roughly look like:

```text
agentic-harness/
│
├── src/
│   ├── agents/
│   │   ├── researcher.py
│   │   ├── analyst.py
│   │   └── critic.py
│   │
│   ├── crews/
│   │   └── research_crew.py
│   │
│   ├── flows/
│   │   └── research_flow.py
│   │
│   ├── tools/
│   │   ├── web_search.py
│   │   ├── calculator.py
│   │   └── company_search.py
│   │
│   ├── knowledge/
│   │   └── knowledge_base.py
│   │
│   ├── guardrails/
│   │   └── policies.py
│   │
│   ├── memory/
│   │   └── memory.py
│   │
│   └── evaluation/
│       └── evaluator.py
│
├── knowledge/
│   ├── architecture.pdf
│   ├── security.pdf
│   └── pricing.pdf
│
├── tests/
│   ├── test_agents.py
│   ├── test_flow.py
│   └── test_tools.py
│
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

# 20. The architecture they should understand

```text
                         USER
                           │
                           ▼
                    ┌────────────┐
                    │ FastAPI/UI │
                    └──────┬─────┘
                           ▼
                 ╔════════════════════╗
                 ║   AGENTIC HARNESS  ║
                 ║                    ║
                 ║      FLOW          ║
                 ║       │            ║
                 ║       ▼            ║
                 ║      CREW          ║
                 ║    ┌──┼──┐         ║
                 ║    ▼  ▼  ▼         ║
                 ║  Rsch Ana Critic   ║
                 ║                    ║
                 ║ ┌────────────────┐ ║
                 ║ │ Tools / MCP    │ ║
                 ║ │ Knowledge/RAG  │ ║
                 ║ │ Memory         │ ║
                 ║ │ Reasoning      │ ║
                 ║ └────────────────┘ ║
                 ║                    ║
                 ║ Guardrails         ║
                 ║ HITL               ║
                 ║ Checkpointing      ║
                 ║                    ║
                 ║ Observability      ║
                 ║ Evaluation         ║
                 ╚════════╤═══════════╝
                          │
                          ▼
                    FINAL REPORT
```

---

# 21. What I would NOT teach in this one-day workshop

This is important.

The CrewAI documentation contains a lot of features, but trying to cover everything will ruin the workshop.

### Skip or provide as optional reading:

* DALL-E/image generation
* every CrewAI tool
* every MCP transport
* Apps
* coding agents
* multimodal deep dive
* custom LLM implementation
* CrewAI AMP deployment
* every observability integration
* advanced CLI features
* Skills deep dive
* training

The versioned docs have all of these areas, but they aren't equally valuable for your **Agentic Harness** objective. ([CrewAI Documentation][1])

---

# 22. The five concepts I would make people remember

At the end, they should remember this:

```text
                 AGENTIC HARNESS
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
      ENABLE          CONTROL         VERIFY
        │               │               │
      Tools           Policy          Traces
      MCP             Guardrails      Metrics
      Knowledge       HITL            Tests
      Memory          Checkpoints     Evaluation
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                     AGENT
                        │
                        ▼
                      CREW
                        │
                        ▼
                      FLOW
```

But the **CrewAI-specific mental model** should be even simpler:

> **Flow controls. Crew collaborates. Agent reasons. Tools act. Knowledge informs. Memory remembers. Guardrails constrain. Observability explains. Evaluation verifies.**

That is a strong workshop narrative, and it is directly aligned with the current CrewAI v1.15.22 architecture rather than forcing a generic multi-agent curriculum onto the framework. ([CrewAI Documentation][1])

### One change I would make from our earlier design

I would **not** make “single Agent → Crew → Flow” merely a linear feature progression.

Make it an architectural discovery:

**“An agent can think. A Crew can collaborate. But a production system needs a Harness around both.”**

That distinction is what will make this workshop substantially more senior-level than a normal CrewAI hands-on session.

[CrewAI v1.15.22 Documentation](https://docs.crewai.com/v1.15.22/en/introduction?utm_source=chatgpt.com)

[1]: https://docs.crewai.com/v1.15.22/en/introduction
[2]: https://docs.crewai.com/v1.15.22/en/concepts/knowledge
[3]: https://docs.crewai.com/v1.15.22/en/concepts/agents
[4]: https://docs.crewai.com/v1.15.22/en/concepts/agent-capabilities
[5]: https://docs.crewai.com/v1.15.22/en/concepts/memory
[6]: https://docs.crewai.com/v1.15.22/en/concepts/processes
[7]: https://docs.crewai.com/v1.15.22/en/concepts/production-architecture
[8]: https://docs.crewai.com/v1.15.22/en/concepts/reasoning
[9]: https://docs.crewai.com/v1.15.22/en/concepts/planning
[10]: https://docs.crewai.com/v1.15.22/en/learn/human-in-the-loop
[11]: https://docs.crewai.com/v1.15.22/en/concepts/checkpointing
[12]: https://docs.crewai.com/v1.15.22/en/observability/tracing
[13]: https://docs.crewai.com/v1.15.22/en/concepts/testing
