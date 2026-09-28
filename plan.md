# Engineering an Agentic Harness with CrewAI — workshop design plan

Status: design draft. This plan turns the [corporate workshop proposal](Proposal/Agentic_Harness_CrewAI_Workshop_Proposal.docx) into a curriculum, build sequence, delivery plan, and acceptance criteria. The proposal remains the source for the audience, one-day format, project, and promised topics. [workshop-outline.md](workshop-outline.md) supplies the beginner-to-advanced learning sequence; the proposal's 9:00–5:30 timing governs this plan where the outline differs.

## 1. Purpose and audience

**Audience:** Engineers, data scientists, architects, and technical leads who can read and edit basic Python. No prior LLM or agent experience is assumed.

**Workshop goal:** Participants build an Enterprise AI Research & Decision Assistant and understand how its agent harness grants capabilities, supplies context, preserves useful state, controls actions, and verifies results.

**Learning promise:** A participant can move from a normal Python function to an LLM call, an agent loop, a tool-using CrewAI agent, a multi-agent Crew, and a stateful Flow. They can explain what each addition solves and diagnose a failure using a trace and tests.

**Format:** One day, 9:00 AM–5:30 PM, with pre-work and 8:30–9:00 arrival checks. Each teaching block follows **show the limitation → explain the concept → edit code → run it → inspect the result**. The finished codebase and production-readiness checklist are take-home deliverables. “Ready for production” is taught as an engineering standard to assess; the one-day lab is a reference implementation, not a production deployment.

## 2. The single project

An employee asks: **“Should our company adopt technology X for enterprise AI?”** The assistant must return a recommendation supported by internal documents and external or supplied research. It should account for a customer constraint recalled from memory and show the evidence behind its answer. If asked to communicate the result to a customer, it must stop for approval before a mock email action runs.

Use one fictional company and technology throughout the day. Provide three short, internally consistent sample documents: architecture, security/compliance, and pricing. Seed one tension between the documents so retrieval, analysis, and critique have something substantive to resolve. Provide a fixed research fixture for the default lab; live web search is an extension because network availability can vary.

### End-to-end behavior

```text
CLI or prepared web shell
    → validate question and customer identity
    → Flow creates/loads typed run state
    → retrieve relevant documents and scoped memory
    → Researcher uses approved tools
    → Analyst weighs evidence; Critic checks claims and gaps
    → Flow validates structured recommendation
       ├─ enough evidence → report
       └─ insufficient evidence → one bounded retry, then explain the gap
    → optional customer communication waits for human approval
    → trace and evaluation record the run
```

The Flow owns branching, state, retries, and approval. Agents choose how to perform bounded research tasks. Tool code owns side effects. The app interface calls the Flow and does not duplicate decision logic.

## 3. Learning ladder and required checkpoints

| Stage | Familiar Python anchor | New idea | Observable checkpoint |
| --- | --- | --- | --- |
| 0. Function | Inputs, branches, return values | Deterministic baseline | A Python function returns a rule-based recommendation from supplied facts |
| 1. Model call | Calling an external function | Prompt, response, uncertainty | Same question produces an LLM answer; participant identifies one unsupported claim |
| 2. Agent loop | `while` loop and callbacks | Model chooses action, receives observation, stops | Participant traces one model → tool → observation cycle before using CrewAI |
| 3. Agent | Object with goal and limits | CrewAI role, task, model, iteration/time limits | One Researcher completes a bounded task with structured output |
| 4. Tools | Typed functions | Agent-visible contract, permission, MCP adapter | Tool call has validated inputs, useful output, and a visible trace |
| 5. Knowledge | Search over a supplied corpus | Chunk, embed, retrieve, cite | Recommendation cites passages from the sample documents |
| 6. Memory | Persisting data beyond a call | Scope and recall across runs | Correct customer's constraint is recalled; another customer's is excluded |
| 7. Crew | Task decomposition | Researcher, Analyst, Critic | Three owned tasks produce a structured recommendation |
| 8. Flow | State machine | Typed state, branch, bounded retry | Missing evidence takes the retry path once; a complete answer reaches report |
| 9. Control | Validation before side effects | Guardrails and human approval | Mock email cannot execute without a recorded approval |
| 10. Recovery | Save and resume | Persistence, checkpoint, safe repeats | A prepared interrupted run resumes without repeating an approved action |
| 11. Verify | Logs and tests | Trace, evaluation set, latency/cost | Participant explains a wrong result from the run record and passes the core checks |

Each stage has a starter state, a reference solution, an expected output, and a recovery checkpoint. A participant who falls behind can resume at the next checkpoint without losing the rest of the day.

## 4. Day schedule: proposal timing retained

| Time | Session | Concept focus | Lab outcome |
| --- | --- | --- | --- |
| 8:30–9:00 | Arrival and environment check | Verify Python, model, embeddings, repository, and sample app | Smoke-test result recorded |
| 9:00–9:20 | Intro: Python → model → agent → harness | Begin with a Python function; show where a plain LLM answer fails; introduce the seven harness concerns | Everyone runs the baseline and marks a missing capability |
| 9:20–10:05 | M1. Agent loop and model choice | Visible loop, prompt/context, role, goal, limits, reasoning/planning, model tradeoffs | One bounded Researcher; inspect its calls and output |
| 10:05–10:50 | M2. Tools and MCP | Python tool contracts, typed inputs, useful results, least privilege, MCP as a connector | Complete one tool, wire two prepared tools, connect a prepared MCP server |
| 10:50–11:05 | Tea break | | |
| 11:05–11:50 | M3. Context and knowledge | Context vs retrieved knowledge vs memory; chunking, embeddings, retrieval, source references | Answer from sample documents and cite the evidence |
| 11:50–12:20 | M4. Memory | Scope, cross-run recall, provenance, retention and privacy | Save a customer constraint; verify scoped recall, isolation, and read-only shared context |
| 12:20–1:15 | Lunch | | |
| 1:15–2:15 | M5. Orchestration: Crew and Flow | Single agent vs specialized team; Crew tasks; typed Flow state, branch and capped retry | Researcher → Analyst → Critic inside a Flow; run pass and insufficient-evidence cases |
| 2:15–3:00 | M6. Control | Input and output validation, prompt injection as untrusted content, approval before a side effect | Invalid request fails early; mock email remains blocked until approval |
| 3:00–3:15 | Tea break | | |
| 3:15–3:35 | M7. Resilience | Timeouts, retries, persistence, checkpoint/resume, idempotent action boundaries | Follow a guided crash/resume demonstration and inspect saved state |
| 3:35–4:15 | M8. Verification | Traces, test fixtures, output and trajectory checks, latency/cost | Trace a run; execute a small evaluation set and fix one failing case |
| 4:15–5:00 | Capstone: fix the broken harness | Diagnose failures by capability, context, memory, intelligence, control, orchestration, and verification | Each pair fixes one or two assigned faults; room debrief covers all eight |
| 5:00–5:15 | Going to production | Readiness checklist, maturity, ownership, operations | Self-assess the completed assistant and identify the next hardening step |
| 5:15–5:30 | Recap, Q&A, feedback | Rebuild the mental model from the running code | Final demo and feedback |

The first 20 minutes and M1 contain the ordinary-Python-to-agent bridge requested for this audience. M2 is the first point where the agent may act outside the model. M5 adds orchestration after participants already understand the pieces it controls.

### Lab pacing within each module

Aim for 5–10 minutes of explanation, 20–30 minutes of editing/running, and 5–10 minutes of inspecting the result and comparing with the checkpoint. The 20-minute resilience block is a guided demonstration. Capstone work is done in pairs to keep it feasible in 45 minutes.

## 5. Module designs and acceptance checks

### Intro and M1 — from Python to an agent

- Show the same question answered by a normal function, a direct LLM call, a visible model/tool loop, and a CrewAI Agent. Keep these four outputs side by side.
- Teach that a prompt is input, an agent loop can choose actions, and the harness sets the available actions and stop conditions.
- Configure a model explicitly, a structured task output, and step/time limits. Reasoning and planning are explained through a short comparison, not required in every lab run.
- **Pass:** Participant can identify which component chose the tool, where the loop stops, and what the structured result contains.

### M2 — tools and MCP

- Three project tools: `search_company_docs` (read-only), `search_research_fixture` (read-only), and `calculate_roi` (pure calculation). Participants implement the calculator contract and finish the two supplied adapters. The company-doc search is later backed by M3 retrieval.
- Include input schemas, descriptions, expected failures, and outputs small enough for the agent to use. An MCP server exposes one prepared read-only research capability; compare its invocation with a local tool.
- Keep customer communication in a separate mock action tool that is unavailable until M6's approval gate.
- **Pass:** A valid tool call returns useful evidence, invalid input is rejected, and the trace shows which tool ran.

### M3 — context and knowledge

- Distinguish the current prompt, the retrieved document passages, the long-lived memory store, and the Flow's run state.
- Load the provided documents, inspect one chunk and embedding configuration, retrieve for a concrete question, and attach source identifiers to claims. Show a deliberately irrelevant retrieval result and its effect on the answer.
- Default guided path: CrewAI Knowledge with a pinned local or approved embedding provider. A direct Qdrant pipeline is an optional extension; CrewAI's Qdrant RAG client is a separate interface from Knowledge's built-in storage.
- **Pass:** At least two material claims in the recommendation point to relevant source passages; missing evidence is called out rather than invented.

### M4 — memory

- Store a customer preference/constraint with explicit customer scope and source. Recall it in a new run and verify a different customer cannot retrieve it. Add a read-only view of seeded shared company policy. Explain how retained memory differs from the Flow state of the current run.
- Use the same verified embedding configuration as the knowledge lab where supported; do not rely on provider defaults.
- **Pass:** The right customer preference and shared policy affect the recommendation; the wrong customer's preference does not, and the agent cannot write to shared policy.

### M5 — Crew and Flow

- Researcher gathers evidence, Analyst weighs adoption criteria, Critic checks unsupported claims and missing risks. Use a sequential process for the core lab; hierarchical management is explained as an alternative.
- Define a typed `DecisionState` with question, customer ID, evidence, draft, validation outcome, retry count, approval status, and final report. Keep only data needed across steps.
- A Flow validates the request, starts the Crew, checks the structured output, retries once if the evidence check fails, then returns either a report or an explicit insufficient-evidence result.
- **Pass:** Both the success path and capped-failure path are demonstrated; no unbounded loop is possible.

### M6 — control

- Validate request shape and tool inputs at boundaries. Treat retrieved text and tool results as evidence, not instructions with authority over the Flow.
- Check the final report's structure and citations. For the mock customer email, persist a proposed action, pause for human approval, and execute only on approval. Record rejection without executing.
- **Pass:** An injected document instruction cannot trigger the mock email; no approval means no action log entry.

### M7 — resilience

- Show the difference between retrying a read-only step and retrying a side effect. Demonstrate an interruption after research and resume from saved state/checkpoint using the pinned CrewAI version.
- Use a stable action ID for the mock email so a resumed run cannot send it twice. If the selected version or storage backend changes resume behavior, the preflight must catch it before the event.
- **Pass:** The resumed report retains completed work and the action log has zero or one execution, never two.

### M8 — observability and evaluation

- Trace Flow step, Crew task, LLM call, retrieval, tool call, validation failure, approval, and duration. Show participants how to answer “Why did this report say yes?” from the trace and cited sources.
- Supply 6–10 test cases: grounded yes/no/uncertain answers, missing evidence, wrong customer scope, invalid tool input, prompt injection, approval denied, bounded retry, and recovery. Use code assertions for objective behavior and a small explicit rubric for synthesis quality.
- Record baseline quality, latency, and call count before and after one change. Use `crewai test` only in a provider configuration verified for that command; the core evaluation path must run on the workshop's chosen model.
- **Pass:** Participant can find one failure in the trace and make a targeted fix that passes the relevant check.

## 6. Capstone fault set

Prepare eight independent, seeded faults, each with a symptom, failing check, trace clue, expected diagnosis, and reference fix:

| Fault | Harness concern | Example symptom |
| --- | --- | --- |
| 1. Wrong tool chosen | Capability | ROI question invokes document search |
| 2. Bad tool schema | Capability/control | Invalid numeric input reaches calculation |
| 3. Missing or irrelevant citation | Context | Recommendation cites the wrong document |
| 4. Cross-customer recall | Memory | Customer B receives Customer A's constraint |
| 5. Unsupported conclusion | Intelligence/verification | Critic accepts a claim absent from evidence |
| 6. Retry loop | Orchestration | Missing evidence triggers repeated Crew runs |
| 7. Approval bypass | Control | Mock email action runs before approval |
| 8. Missing trace span | Verification | Tool activity cannot be explained from run record |

For 100–150 participants, assign different faults to pairs or tables. Each group repairs one or two, then the facilitator walks through all eight. Requiring every attendee to repair all eight in 45 minutes would conflict with the proposal's one-day beginner-to-advanced format.

## 7. Repository and learning materials to build

```text
workshop/
  README.md                 # setup, run commands, checkpoint map
  pyproject.toml            # pinned, tested dependencies
  .env.example              # names only; no credentials
  docker-compose.yml        # optional pretested supporting services
  src/decision_assistant/
    baseline.py             # ordinary Python comparison
    model_call.py           # direct LLM comparison
    agent_loop.py           # visible loop teaching aid
    agents.py               # Researcher, Analyst, Critic
    crew.py                 # owned tasks and structured outputs
    flow.py                 # state, branching, retry, approval
    tools.py                # read-only tools and mock action
    knowledge.py            # document retrieval and references
    memory.py               # scoped recall
    observability.py        # run IDs and trace setup
    app.py                  # CLI or prepared API/UI shell
  knowledge/sample/         # fictional, internally consistent docs
  mcp_server/               # prepared read-only local server
  labs/                     # lab instructions and expected outputs
  checkpoints/              # runnable recovery states, lab 0–8
  capstone/                 # eight seeded faults and instructor key
  tests/                    # deterministic checks and evaluation cases
  slides/                   # diagrams and concept examples
  handouts/                 # one-page recap and readiness checklist
```

Lab instructions need a fixed pattern: starting checkpoint, objective, edit target, commands, expected output, one deliberate failure to inspect, and recovery link. Instructor notes add timing, common failure symptoms, and a fallback demonstration. Slides should show the exact object or trace participants will inspect in the next lab.

## 8. Model, data, and environment design

- Pin Python and CrewAI versions and verify all labs on the same combination. The proposal says Python 3.10 or later; choose one tested version as the default installation target.
- Offer one **primary** model path for the event: a tested local Ollama model if machines can run it at acceptable speed, or a company-approved hosted API. Keep one fallback path ready. Test the chosen model's tool calling and structured output before committing to it. The proposal's “8 GB RAM” is a starting assumption, not a performance guarantee.
- Configure an embedding model separately for Knowledge and Memory. Verify that no default provider makes an unexpected external call in the local path.
- Use fictional sample documents by default. Company documents are an opt-in replacement only after the company confirms a provider, permitted content, and an ingestion rehearsal. The workshop can succeed entirely on samples.
- Keep research fixture and email action local for the required labs. Any live search, external MCP service, or real email is outside the required path.
- Keep the proposal's Planner-agent demonstration as an optional extension: it reads the knowledge folder and drafts a structured proposal using the same memory and guardrail boundaries.
- Ensure each attendee can see their own run state, memory scope, and trace. Use unique sample customer/run IDs; reset scripts must target only workshop data.
- Provide a no-install or prebuilt environment option if 100–150 laptops, mixed operating systems, or corporate network controls make local setup unreliable.

## 9. Pre-work and delivery operations

### One week before

1. Confirm date (proposal offers 17 or 24 October 2026), venue/online format, expected headcount, and target laptop/OS mix.
2. Confirm local versus approved hosted model, network access, and whether sample or approved company documents will be used.
3. Send pinned setup guide, repository, model/embedding setup, and one-command smoke test. Collect only the test result and non-sensitive error details.
4. Rehearse every checkpoint and the complete capstone on the same network and machine class participants will use.

### Delivery staffing and room

The proposal's cover estimates **100–150 participants**, while its logistics section says **30 or fewer** gives the best hands-on support and offers only **1–2 helpers**. These are different delivery modes and must be reconciled before the event. For a group near 100–150, plan pair work, table-level support, a visible help queue, checkpointed code, and staffing based on a rehearsal of setup failure rates. A single facilitator plus 1–2 helpers should be treated as the small-room plan, not assumed sufficient for the larger audience.

Require projector/screen, reliable Wi-Fi, power at every table, and a local or mirrored source for large model downloads if Ollama is selected. Confirm the two breaks and lunch timing with the venue.

### Day-of roles

- **Facilitator:** Explain concepts, run demos, hold the timing, and lead the final diagnosis.
- **Lab helpers:** Triage setup failures and unblock participants at checkpoints without completing their exercises for them.
- **Room/technical contact:** Handle network, display, power, and access issues. Name this contact before the event.

## 10. Build plan and gates

1. **Curriculum lock:** Agree on audience baseline, default model path, delivery mode, and sample data. Freeze the learning ladder and module outcomes.
2. **Golden path prototype:** Build the full assistant once, including the Flow, approval boundary, trace, and six core evaluation cases. Verify it works end to end before splitting it into labs.
3. **Lab extraction:** Create starter and solution checkpoints from the golden path. Ensure each checkpoint runs independently and that the next lab starts from the previous result.
4. **Instructor assets:** Create slides, diagrams, answer key, troubleshooting guide, one-page recap, and production-readiness checklist.
5. **Technical rehearsal:** Run setup from a clean laptop, execute all labs with the pinned versions and chosen model, time each module, and test a failed-network and failed-model fallback.
6. **Pilot:** Have at least one basic-Python learner complete the labs without the author driving. Record where instructions, timing, or expected outputs fail; revise.
7. **Event readiness gate:** No broken checkpoint; capstone faults reproducible; sample path works without company data; model and embedding costs/limits known; support plan matches headcount.

## 11. Completion and readiness measures

### Participant completion

At the end, a participant or pair can run the end-to-end question and show: a source-backed recommendation, correct scoped recall, a bounded retry result, blocked/approved mock action, a trace, and passing core checks. They can point to the code that controls each behavior.

### Instructor readiness

Every module has tested instructions, a starter and solution state, expected output, a known recovery path, and an allotted duration proven in rehearsal. The demo works from a clean setup on the selected model path.

### Production-readiness checklist taught at close

Assess permissions and tool scope; evidence quality; memory isolation and retention; input/output contracts; action approval; retry and resume safety; trace coverage; evaluation quality; model/provider cost and latency; secrets and data handling; deployment ownership; and rollback/recovery. Mark each as implemented in the lab, demonstrated, or future production work.

## 12. Decisions to close before building lab code

| Decision | Default for design | Needed from sponsor/organizer |
| --- | --- | --- |
| Date and format | 9:00–5:30, in person | Select 17 or 24 October 2026, venue or online, and final hours |
| Headcount | Labs in pairs with checkpoints | Confirm whether delivery is ~30 or 100–150; staff and room accordingly |
| Model | Tested local model and embedding pair, hosted fallback | Confirm laptop capacity, approved provider, and network policy |
| Documents | Fictional sample set | Confirm whether approved non-sensitive company documents replace samples |
| Interface | CLI core with prepared optional web shell | Confirm whether a visible web UI is required for the final demo |
| Post-event support | Slides, repository, recap, checklist | Confirm any Q&A window and distribution method |

These decisions change delivery logistics or provider setup. They do not block drafting the curriculum, sample data, golden path, or lab structure.

## References for technical design

- [CrewAI production architecture](https://docs.crewai.com/v1.15.22/en/concepts/production-architecture) for Flow state/control and focused Crews.
- [CrewAI Knowledge](https://docs.crewai.com/v1.15.22/en/concepts/knowledge) and [Memory](https://docs.crewai.com/v1.15.22/en/concepts/memory) for retrieval, scopes, and explicit embedding setup.
- [CrewAI checkpointing](https://docs.crewai.com/v1.15.22/en/concepts/checkpointing) and [testing](https://docs.crewai.com/v1.15.22/en/concepts/testing) for the resilience demo and provider-specific test command.
- [Anthropic, Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) for the progression from model calls to workflows and agents.
- [Anthropic, Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) and [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) for tool contracts and evaluation design.
- [OpenAI, Harness engineering](https://openai.com/index/harness-engineering/) for inspectable context, traces, and feedback loops. Its software-engineering-agent setting informs the design principle; this workshop applies it to a decision assistant.
