---
marp: true
theme: default
paginate: true
---

# Engineering an Agentic Harness with CrewAI

From normal Python to a controlled, observable decision assistant

---

# Today's outcome

One question. One system. A new capability at each step.

By the end: source-backed recommendation, scoped memory, bounded workflow, approval gate, trace, and tests.

---

# Start with Python

```text
inputs → function → predictable output
```

What can a fixed rule answer? What evidence can it not synthesize?

Open `01-python-to-llm`.

---

# Add a model

```text
prompt → model → fluent answer
```

Fluency does not prove a claim. Keep one unsupported claim visible throughout the day.

---

# The agent loop

```text
task → model → tool? → observation → model → answer
```

The model chooses a next step. The harness chooses which tools exist and when the loop stops.

Open `02-agent-loop`.

---

# Capability: tools and MCP

Local Python function or MCP-connected function; both need clear inputs, useful outputs, and bounded permissions.

Open `03-tools` and `04-mcp`.

---

# Context, Knowledge, Memory, State

| Name | Meaning |
| --- | --- |
| Context | What this run sees now |
| Knowledge | Retrieved reference material |
| Memory | Facts retained across runs |
| Flow state | Current workflow's typed progress |

Open `05-knowledge` and `06-memory`.

---

# One agent or a Crew?

Researcher finds evidence. Analyst weighs it. Critic checks it.

Use a Crew when role separation improves the result enough to justify the extra calls.

Open `07-crews`.

---

# Flow controls the work

```text
validate → Crew → evidence check ┬→ report
                                  └→ retry once → explain gap
```

Open `08-flows`.

---

# Approval belongs at the action boundary

```text
proposed email → human approval → mock action
```

The model cannot approve its own side effect. Open `09-control`.

---

# A crash is part of the design

Checkpoint completed work. Resume carefully. Give every side effect an idempotency key.

Open `10-resilience`.

---

# Explain and verify

A trace answers “what happened?” Tests answer “did the boundary hold?”

Inspect Crew, model, tool, and Flow events. Run the evidence and approval checks.

Open `11-observability` and `12-evaluation`.

---

# Capstone

Run the complete assistant. Fix one or two seeded failures. For each one:

```text
symptom → trace/check → responsible layer → repair → rerun
```

Open `13-project` and `14-capstone`.

---

# Going to production

Check tool scope, evidence, memory isolation, approval, recovery, traces, evaluation, and provider/data policy.

Use the production-readiness checklist to name the next engineering task.
