# Agentic harness: one-page recap

An ordinary Python function follows a fixed path. An LLM can synthesize an answer. An agent can choose actions and inspect results. A Crew divides a complex task among agents. A Flow controls the state and path around that work.

```text
User → Flow (validate, state, route, approve)
          → Crew (Researcher → Analyst → Critic)
              → model + tools + Knowledge + Memory
          → evidence check → report or bounded retry
          → trace + evaluation
```

| Question | Harness component | Workshop proof |
| --- | --- | --- |
| What can it do? | Tools and MCP | ROI and document research tools |
| What does it know now? | Context and Knowledge | Retrieved passages with source IDs |
| What does it remember? | Scoped Memory | Customer-specific preference across runs |
| What work happens next? | Crew and Flow | Owned tasks, branch, capped retry |
| What may happen? | Validation and approval | Mock email blocked before approval |
| What happened? | Trace | Crew/LLM/tool event sequence |
| Was it good enough? | Tests and evaluation | Evidence, isolation, and action checks |

When a result is wrong: reproduce it, read the trace and state, identify the failing boundary, fix the smallest cause, then rerun the relevant case. A better prompt alone does not repair a missing permission gate or an invalid source ID.
