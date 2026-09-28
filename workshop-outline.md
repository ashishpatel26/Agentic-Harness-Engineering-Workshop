# Engineering an Agentic Harness with CrewAI

## Zero-to-hero workshop outline — draft 1

**Audience:** Engineers, data scientists, architects, and technical leads who know basic Python but have no agent experience.  
**Format:** One day, 9:00 AM–5:30 PM; short explanations followed by guided labs.  
**Project:** Build an Enterprise AI Research & Decision Assistant, one capability at a time.  
**End result:** A working app that accepts a question, uses approved tools and documents, coordinates a small Crew through a stateful Flow, requests approval for a sensitive action, and exposes traces and test results.

### Learning path

```text
Ordinary Python program
  → Python program that calls an LLM
  → Visible model/tool/observation loop
  → CrewAI agent that chooses its next step
  → Agent with bounded tools
  → Agent grounded in documents
  → Agent with scoped memory
  → Crew with specialized tasks
  → Flow that controls the Crew
  → Approval, traces, and tests
  → Working end-to-end application
```

Introduce the word **harness** after participants have experienced the limits of an unconstrained agent. Its parts then answer concrete questions: What can the agent do? What does it know? What may it do? What happened? Was the result good enough? A Flow is the orchestration part of this harness; the harness also includes the tool boundary, context, memory, approval, and feedback mechanisms.

## Schedule and lab checkpoints

| Time | Module | Concept from familiar Python | Participant builds or verifies |
| --- | --- | --- | --- |
| 8:30–9:00 | Arrival and setup | Run a Python script | Environment smoke test; starter app and model respond |
| 9:00–9:25 | 1. From Python function to AI workflow | Inputs, functions, return values, exceptions | A deterministic function that assembles a technology decision from supplied facts; identify where fixed rules fall short |
| 9:25–10:05 | 2. First LLM call | A function call with a less predictable result | Ask the same question through an LLM; inspect prompt, response, latency, and an unsupported claim; record one baseline check |
| 10:05–10:45 | 3. From model call to agent loop | A loop: choose action → call tool → inspect result → continue or stop | Walk through a tiny visible tool loop, then configure one CrewAI researcher with a goal, task, model, step limit, and structured output |
| 10:45–11:00 | Break | | |
| 11:00–11:45 | 4. Tools and MCP | Typed Python functions and external interfaces | Implement one read-only calculation or lookup tool with a clear input/output contract; inspect tool selection, arguments, and returned evidence; connect to a prepared MCP tool in a guided extension |
| 11:45–12:30 | 5. Context and knowledge | Passing data into a function versus searching a document set | Add sample company documents, retrieve relevant passages, and return an answer with source references |
| 12:30–1:15 | Lunch | | |
| 1:15–1:45 | 6. Memory | Local variables versus data retained for later requests | Store and recall a customer constraint in a scoped memory; show that a new run can use it and another customer cannot |
| 1:45–2:30 | 7. From agent to Crew | Splitting a job into owned tasks | Add an analyst and critic; compare a single-agent answer with the Crew's structured recommendation and decide whether the extra agents improved it |
| 2:30–3:15 | 8. Flow orchestrates the harness | A state machine with branches and bounded retries | Wrap the Crew in a typed Flow: validate request → research → check evidence → report or retry once |
| 3:15–3:30 | Break | | |
| 3:30–4:05 | 9. Control and human approval | Validation before a side effect | Reject an invalid request or report; require explicit approval **before** a mock email action executes |
| 4:05–4:40 | 10. Trace, test, evaluate | Logging, assertions, and test cases | Inspect one complete trace; run deterministic checks and score a small answer set for evidence, accuracy, and action safety |
| 4:40–5:10 | 11. End-to-end capstone | Integrating and debugging a program | Use a prepared API/UI wrapper to run the complete assistant; diagnose and repair one seeded harness failure |
| 5:10–5:30 | 12. Review and next steps | From working demo to reliable service | Demonstrate the finished path; explain where persistence, checkpoint/resume, deployment, and operational limits fit |

## The project as it grows

The same user question runs throughout the day: **“Should our company adopt technology X?”** Sample architecture, security, and pricing documents provide evidence. A mock customer communication gives the approval gate a real consequence without sending anything externally.

Each stage has a runnable checkpoint. Participants can compare their result with a reference run before moving on. The starter repository supplies model configuration, sample documents, an MCP server, and an API/UI shell so lab time stays focused on the agent and harness concepts. The final application calls the Flow; it does not contain a second, separate implementation of the decision logic.

### Required end-of-day behavior

1. Validate the user's question and preserve its state through the run.
2. Retrieve relevant company evidence and cite the source material in a structured recommendation.
3. Use a bounded tool and a Researcher → Analyst → Critic Crew where each role has a clear task.
4. Branch when evidence is insufficient, retry at most once, and explain failure if the check still fails.
5. Recall only the appropriate customer's saved preference or constraint.
6. Stop at an approval gate before the mock email action.
7. Show what the model, retrieval, tool, Crew, and Flow did in a trace.
8. Run a small set of checks that can catch an unsupported answer or unauthorized action.

## Teaching decisions to settle before writing labs

- **One supported model path:** Pin CrewAI and model versions; provide a verified local-model configuration or a verified hosted-provider configuration. Configure embeddings separately so knowledge and memory work with the chosen path.
- **One default retrieval path:** Use CrewAI Knowledge storage in the guided lab. Treat a direct Qdrant retrieval pipeline as an extension because the Qdrant RAG client and Knowledge's built-in storage are distinct interfaces.
- **A simple evaluation path:** Define one expected behavior during the first LLM lab, then use a supplied test set and explicit scoring rules in the verification lab. Demonstrate framework evaluation commands only with a provider setup known to support them.
- **Prepared infrastructure:** API/UI, sample documents, MCP server, and optional tracing backend should be running or smoke-tested before the teaching day. Participants still connect and inspect each layer.
- **Recovery as an extension:** Demonstrate persistence and checkpoint/resume after the main capstone, or provide it as an advanced lab. It should not be required to finish the end-to-end path.
- **Large-room support:** If attendance is near the proposal's 100–150 estimate, use pairs, checkpointed starter code, visible expected outputs, and enough lab support for setup failures.

## Success criterion

A participant who began with ordinary Python can explain the change at every step, run the complete assistant, point to the code that grants capability or enforces control, and use a trace plus tests to diagnose a wrong result.

## Sources informing the outline

- [CrewAI production architecture](https://docs.crewai.com/v1.15.22/en/concepts/production-architecture): Flow for state and predictable control; Crew for focused autonomous work.
- [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): distinguish fixed workflows from model-directed agents, expose the underlying loop, and add complexity only when it improves the task.
- [Anthropic, Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents): design tool interfaces and responses for an agent, then test whether the agent uses them correctly.
- [Anthropic, Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents): define success early and assess both the result and the trajectory.
- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/): make context, application behavior, logs, and validation legible to agents and engineers. Its example concerns coding agents; the workshop applies the same inspectability principle to a decision assistant.
- [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): save clear progress artifacts for work that spans sessions; this informs the optional checkpoint and recovery lab.
