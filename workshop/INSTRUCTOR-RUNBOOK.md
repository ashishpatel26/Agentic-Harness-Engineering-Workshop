# Instructor runbook

Use [plan.md](../plan.md) for full objectives and the proposal's schedule. This runbook is the day-of checklist for the numbered code folders.

## Before participants arrive

- Verify the exact `uv.lock`, Python 3.12, chat model, embedding model, MCP server, and the 15 core notebook/script pairs on a target laptop. Rehearse the eight advanced pairs separately if teaching the extension.
- Rehearse the 9:00–5:30 schedule using a fresh environment. Keep a solution copy and a clean copy of the repo.
- Start a help queue. For 100–150 attendees, arrange table-level support and pair work before opening the room.
- Keep fictional sample documents as the default. Approved company documents are optional and must be tested separately.

## Teaching loop

Each topic begins with the notebook's **Problem → Concept → Architecture** cells. Run the first code cell, ask participants to predict the next observable event, then run the rest. Ask them to do the **Your turn** exercise and compare with its checkpoint. The same-name `.py` file is a fallback if notebooks fail.

| Proposal slot | Open these folders | Observable proof |
| --- | --- | --- |
| Intro, 9:00–9:20 | `00-verify`, `01-python-to-llm` | Python rule and model answer differ; unsupported claim identified |
| M1, 9:20–10:05 | `02-agent-loop` | Agent has role, task, limits, and a visible model/tool loop |
| M2, 10:05–10:50 | `03-tools`, `04-mcp` | Local and MCP tools both expose typed, bounded capabilities |
| M3, 11:05–11:50 | `05-knowledge` | Retrieved sample documents support source-labeled claims |
| M4, 11:50–12:20 | `06-memory` | Customer A and B are recalled from separate scopes |
| M5, 1:15–2:15 | `07-crews`, `08-flows` | Specialized tasks plus success/evidence-gap Flow routes |
| M6, 2:15–3:00 | `09-control` | Invalid input and unapproved action are blocked |
| M7, 3:15–3:35 | `10-resilience` | Saved checkpoint path and resume mechanism inspected |
| M8, 3:35–4:15 | `11-observability`, `12-evaluation` | Local trace and deterministic evaluation results |
| Capstone, 4:15–5:00 | `13-project`, `14-capstone` | End-to-end report; assigned faulty checks repaired |

**Bonus scenarios.** Each basic lesson ends with an optional bonus cell that applies the same concept to a lighter, different problem (a trip, a job ad, a party order). They are listed in the [README](README.md#bonus-scenarios-one-per-basic-lesson). Use them as the "Your turn" demo when the room is ahead; skip them when behind. The no-model ones (8 Flow, 10 Resilience, 12 Evaluation) always run in seconds. On a local 4B model the model-backed ones can take one to five minutes, and the Knowledge (5) and Crew (7) bonuses are the slowest, so run those as a demonstration rather than hands-on.

**Slow or empty model answers.** Thinking-capable local models can spend the whole output budget on hidden reasoning and return an empty answer ("Invalid response from LLM call - None or empty"), or take minutes for one call. In the authoring test on a Windows laptop, `ollama/qwen3.5:4b` returned an empty answer after 330 s for a one-line prompt, and CrewAI's `LLM` does not accept a `think=False` switch, while `ollama/qwen2.5:7b` (not a thinking model) answered the same prompt in 30 s. If a lesson stalls, rerun it once, then switch to a non-thinking model without editing code: set `WORKSHOP_MODEL=ollama/qwen2.5:7b` in `.env` (after `ollama pull qwen2.5:7b`). Rehearse every model-backed lesson on the actual workshop model before the day.

The resilience slot is a guided demonstration. It requires timing the interruption after task one; do not make every attendee repeat a slow local model run. In the capstone, assign one or two faults to each pair and use `14-capstone/INSTRUCTOR.md` for the whole-room debrief.

## Advanced follow-up (optional second session)

Run only after the basic path. Each lesson extends one basic step; open the basic notebook first as a reminder, then the advanced one.

| Order | Advanced folder | Extends basic step | Observable proof |
| --- | --- | --- | --- |
| 1 | `17-lancedb-rag` | 5 Knowledge | Real source IDs, distinct from CrewAI Knowledge |
| 2 | `19-nemo-guardrails` | 9 Control | Input/output checks stay outside authorization |
| 3 | `18-state` | 10 Resilience | Approvals survive restart; cache is disposable |
| 4 | `20-langfuse` | 11 Observability | Remote trace appears; local trace works offline |
| 5 | `21-ragas` | 12 Evaluation | Quality score kept separate from safety gates |
| 6 | `15-api`, `16-ui`, `22-podman` | 13 Project | Requests cannot approve their own action; UI shows cited evidence; Compose describes the services |
| 7 | `14-capstone` | all | Assigned faults repaired; whole-room debrief |

Steps 1–4, 6, 7 and 8 have no advanced follow-up. `14-capstone` is in the basic day's 4:15–5:00 slot; use it as the closing exercise of the advanced session only if the basic day did not reach it. The advanced folders need live services (Ollama embeddings, Postgres, Redis, Langfuse, Podman); rehearse them separately.

## Recovery and escalation in the room

If a model call fails, first check the 00 smoke test, then the model server, model names, and `.env`. If the chat model works but Knowledge or Memory fails, check the embedding model separately. If an MCP lesson fails, run the server connection without an agent and check that stdout has only protocol traffic. If a participant falls behind, provide the next numbered folder; the lessons are runnable independently.

Never switch providers silently or send a participant's document text to an unapproved hosted service. The default corpus and research fixture make the full lesson path possible with fictional data.

## Close

Have one pair explain a claim using the document citation, one explain a tool event in the trace, and one explain the approval gate. Distribute the recap and readiness checklist. Collect which checkpoints each pair completed and which failures consumed time so the next run can be improved.
