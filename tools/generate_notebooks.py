"""Regenerate teaching notebooks from the matching percent-format Python files.

Numbered lesson scripts remain the executable source. Notebook-only teaching
notes expand each script into the reference workshop's problem → concept →
architecture → steps → failure mode progression without duplicating code.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Each guide gives the notebook the same teaching arc as the supplied sample:
# problem, concept, architecture, exercise, and a concrete success check.
GUIDES: dict[str, tuple[str, str, str, str, str]] = {
    "00-verify": (
        "A classroom lab fails when model setup is discovered mid-session.",
        "A smoke test separates package, chat-model, and embedding setup.",
        "uv environment → CrewAI import → configured LLM → short response",
        "Run the cells and identify which dependency fails, if any.",
        "CrewAI imports, the model replies, and the embedding provider is explicit.",
    ),
    "01-python-to-llm": (
        "A fixed Python rule can compare numbers but cannot explain uncertain evidence.",
        "A model call adds synthesis while making factual verification necessary.",
        "facts → Python function / CrewAI LLM → compare outputs and unknowns",
        "Change one missing fact and compare the two answers.",
        "You can point to a claim the model could not know from its input.",
    ),
    "02-agent-loop": (
        "A one-shot answer cannot request and inspect new evidence.",
        "An agent loop alternates model decisions and observations until a stop condition.",
        "task → model → action? → tool → observation → model → answer",
        "Find the maximum iteration setting and explain what it prevents.",
        "You can name the role, task, observation, and stopping bound.",
    ),
    "03-tools": (
        "The model cannot calculate from a trusted function unless that function is exposed.",
        "A CrewAI tool wraps a typed Python contract the agent may invoke.",
        "task → agent chooses ROI tool → validated inputs → scenario result",
        "Try a zero annual cost in the pure function before the agent run.",
        "Invalid cost fails, and the model labels the valid ROI as a scenario.",
    ),
    "04-mcp": (
        "A local tool and a separately hosted capability need different connection lifecycles.",
        "MCP supplies a standard tool connection; CrewAI still presents a tool to the agent.",
        "CrewAI adapter ↔ stdio MCP server → annual_roi function",
        "List the server's tools, then compare their names with the local tool lesson.",
        "The adapter discovers annual_roi and closes its subprocess after use.",
    ),
    "05-knowledge": (
        "A fluent answer may omit the company documents or invent vendor claims.",
        "CrewAI Knowledge retrieves relevant document chunks using a configured embedder.",
        "sample documents → chunks/embeddings → Knowledge retrieval → agent answer",
        "Ask about deletion guarantees and inspect whether the answer admits the gap.",
        "Answer claims name source IDs and identify unverified facts.",
    ),
    "06-memory": (
        "A new run does not automatically know a customer's saved constraint.",
        "CrewAI Memory recalls retained facts; explicit scopes separate customers.",
        "customer A/B facts → scoped store → scoped recall in a later run",
        "Search both scopes for deployment preferences and inspect the memory tree.",
        "A's VPC preference does not appear in B's recall.",
    ),
    "07-crews": (
        "One agent may research, decide, and self-review without a clear handoff.",
        "A sequential Crew assigns evidence, analysis, and critique to specialists.",
        "Researcher → Analyst → Critic → structured DecisionReport",
        "Compare the final report with the one-agent answer from lesson 02.",
        "The report contains a conditional recommendation, citations, risks, and next steps.",
    ),
    "08-flows": (
        "Crew collaboration alone does not define request validation or failure routing.",
        "A typed Flow owns state, branches, and a bounded retry around the Crew.",
        "validate → Crew → evidence check → report or insufficient-evidence route",
        "Inspect retry_count and predict the branch for a report with one source.",
        "The run ends with a report or an explicit gap after at most two attempts.",
    ),
    "09-control": (
        "An agent's answer must not authorize its own customer-facing side effect.",
        "Validation and human approval are executable boundaries outside the model.",
        "request → validation → report check → approval gate → mock action",
        "Run the denied, approved, and repeated-action cases in order.",
        "Denied writes nothing; approved writes one local record; repeat writes no second record.",
    ),
    "10-resilience": (
        "A long task may stop after completing useful work.",
        "CrewAI checkpoints can restore progress; side effects still require idempotency.",
        "task 1 → checkpoint → interruption → restore → task 2",
        "Interrupt after task one, locate the saved checkpoint, and resume with its path.",
        "Completed research is reused and no mock action is duplicated.",
    ),
    "11-observability": (
        "A final answer alone cannot explain tool choice or execution order.",
        "CrewAI events expose execution milestones; a local listener records a minimal trace.",
        "Crew/LLM/tool events → local JSONL trace → diagnosis",
        "Find the first model event and each tool event in the trace.",
        "You can reconstruct the key run sequence without reading hidden prompts.",
    ),
    "12-evaluation": (
        "A polished answer can still bypass approval or contain invalid citations.",
        "Objective checks encode non-negotiable behavior before subjective scoring.",
        "test cases → deterministic checks → pass/fail evidence",
        "Add a case for a report containing an unknown source ID.",
        "A failing case identifies a specific harness boundary to repair.",
    ),
    "13-project": (
        "The pieces must work together behind one entry point.",
        "The CLI invokes the existing CrewAI Flow; it does not duplicate decision logic.",
        "question/customer/approval → Flow → Crew → report/action route",
        "Run a report, then request a mock email without and with approval.",
        "The report has sources and only explicit approval records the mock action.",
    ),
    "14-capstone": (
        "Agent failures can arise in different harness layers but look similar at the output.",
        "Use a failing check to identify the boundary, then make the smallest repair.",
        "symptom → failing case → responsible layer → repair → rerun",
        "Fix one or two assigned faults and explain the evidence behind your diagnosis.",
        "Your assigned checks pass and the repair does not weaken another boundary.",
    ),
}

# Diagrams name the actual CrewAI boundary in each lesson. Arrows represent
# data/control transfer, not a claim that the model can directly call Python.
ARCHITECTURES = {
    "00-verify": """uv sync ──▶ Python kernel ──▶ CrewAI import
                                 ├──▶ chat LLM ──▶ short response
                                 └──▶ embedder ──▶ vector dimensions""",
    "01-python-to-llm": """same evidence ──┬──▶ fixed Python rule ──▶ fixed decision
               └──▶ CrewAI LLM call ──▶ prose + possible unsupported claims
                                      │
                                      └──▶ human checks evidence""",
    "02-agent-loop": """task ──▶ Agent / LLM ──▶ choose action? ──yes──▶ tool
             ▲                                   │        │
             │                              observation ◀┘
             └──────── repeat until answer or max_iter ──────────""",
    "03-tools": """Crew Task ──▶ Agent ──▶ typed ROI tool request
                  ▲                    │
                  │               Python validation
                  │                    │
                  └──── observation ◀──┘
                 Agent ──▶ scenario answer + caveat""",
    "04-mcp": """Crew Task ──▶ Agent ──▶ MCPServerAdapter
                              │ starts stdio subprocess
                              ▼
                        FastMCP server ──▶ annual_roi
                              │ JSON tool result
                              └───────────────▶ Agent answer""",
    "05-knowledge": """company files ──▶ Knowledge sources ──▶ chunks + embedder
                                               │ retrieval
user question ──▶ Crew / Researcher ◀──────────┘
                         └──▶ answer + source IDs + unknowns""",
    "06-memory": """customer A fact ──▶ /customer/customer-a ──┐
                                           ├──▶ scoped recall ──▶ next run
customer B fact ──▶ /customer/customer-b ──┘
                  (B's facts must not enter A's context)""",
    "07-crews": """question + customer context
          │
          ▼
Researcher (tools + knowledge) ──▶ evidence notes
          ▼
Analyst (ROI scenario) ──▶ conditional recommendation
          ▼
Critic (source check) ──▶ DecisionReport""",
    "08-flows": """request ──▶ validate ──▶ Research Crew ──▶ report check
                               ▲                    │
                               └── retry, at most 1 ┘
                                             │
                           valid ──▶ report / approval route
                         invalid ──▶ evidence-gap route""",
    "09-control": """input ──▶ validate_question ──▶ Crew report
                                      │
                               validate_report
                                      │
                           approval? ──no──▶ blocked
                               │ yes
                               ▼
                         idempotent mock email""",
    "10-resilience": """task 1 ──▶ checkpoint file ──▶ task 2
               │ interruption         ▲
               └──▶ restore path ──────┘
side effect ──▶ separate idempotency key (checkpoint alone is insufficient)""",
    "11-observability": """Crew start ──▶ LLM events ──▶ tool events ──▶ Crew end
      │               │                │              │
      └───────────────┴────────────────┴──────────────┘
                         local JSONL trace""",
    "12-evaluation": """known cases ──▶ deterministic harness checks
                   ├──▶ ROI contract
                   ├──▶ report/source contract
                   └──▶ approval boundary
                              │
                         PASS / FAIL""",
    "13-project": """CLI request ──▶ run_assistant ──▶ scoped Memory
                    │                  │
                    ▼                  ▼
                DecisionFlow ──▶ Research Crew ──▶ DecisionReport
                    │
                    └──▶ approval gate ──▶ local mock action""",
    "14-capstone": """symptom ──▶ failing test ──▶ trace responsible boundary
                                  │
                      minimal repair + rerun
                                  │
                      no new regression? ──▶ explain""",
}

FAILURES = {
    "00-verify": "A working chat response does not prove embedding works. Test both before teaching; a missing Ollama model or endpoint should be diagnosed here, not in the Knowledge lab.",
    "01-python-to-llm": "The model may present the missing deletion guarantee as a fact. A fluent answer is not evidence; write down which input sentence supports each claim.",
    "02-agent-loop": "Without a stop bound, repeated tool choices consume time and tokens. `max_iter` and `max_execution_time` cap the CrewAI run; the deterministic loop makes that bound visible.",
    "03-tools": "The model selects tools from their names/descriptions, but Python must still reject invalid arguments. Test the pure function before involving the model.",
    "04-mcp": "The adapter's context manager owns the server connection. A stray server `print()` corrupts stdio protocol messages; a missing tool name means discovery failed before the LLM ran.",
    "05-knowledge": "Retrieval can return an irrelevant chunk or no chunk. Source IDs in prose are not automatic proof: verify them against the actual documents and explicitly report missing evidence.",
    "06-memory": "Using a global scope leaks one customer's fact into another customer's run. The scope identifier is a security boundary, not a personalization convenience.",
    "07-crews": "More agents add latency and can repeat an unsupported claim. The Critic must check named sources and the final report must be validated outside the model.",
    "08-flows": "A weak report should not be retried forever. The Flow stops after two attempts and reports an evidence gap; a failed run is a valid controlled outcome.",
    "09-control": "Never treat an agent's request as human approval. An action must pass validation and an external approval flag; retries must reuse an idempotency key.",
    "10-resilience": "Restoring a checkpoint can repeat a side effect performed just before interruption. Keep the action boundary idempotent independently of CrewAI checkpoints.",
    "11-observability": "A trace that logs full prompts can leak private documents. This local listener records event types and timestamps; record sensitive payloads only under an explicit data policy.",
    "12-evaluation": "A prose-quality score cannot catch a bypassed approval gate. Keep deterministic safety checks as release blockers and use model-judged scores only as an additional signal.",
    "13-project": "A good final report does not imply the action route is safe. Exercise the no-approval path, approved path, and replay of the same action ID separately.",
    "14-capstone": "Fixing the visible answer without repairing the responsible layer can hide the fault. Reproduce, isolate the boundary, patch, and rerun the relevant regression checks.",
}

CONCEPT_DETAILS = {
    "00-verify": "There are two model dependencies: a chat model for generation and an embedding model for semantic retrieval. Passing one check does not imply the other works.",
    "01-python-to-llm": "A Python function maps explicit inputs to a repeatable output. An LLM can synthesize language across incomplete inputs, but its response is probabilistic and must be checked against the evidence supplied.",
    "02-agent-loop": "An agent adds a feedback loop around the model: propose an action, run it through the harness, append the observation, then decide whether to continue. The model requests; the runtime executes.",
    "03-tools": "CrewAI exposes a Python function through a schema and a natural-language description. The model sees the contract and can request a call; the runtime validates arguments and executes the function.",
    "04-mcp": "MCP is a transport and discovery boundary, not a new reasoning model. A separate server publishes a tool; CrewAI's adapter converts the discovered capability into a tool an Agent can use.",
    "05-knowledge": "Knowledge is retrieved source material, not conversation history. Chunking and embeddings select relevant passages; source IDs let a reviewer connect an output claim back to an input document.",
    "06-memory": "Memory retains selected facts across invocations. A scoped recall narrows what is eligible to be returned, so customer identity must be chosen by the application, never guessed from the prompt.",
    "07-crews": "A Crew groups specialist Agents and Tasks. Sequential process plus explicit task context establishes a handoff; a structured final output makes the decision easier to validate.",
    "08-flows": "The Flow is deterministic orchestration around probabilistic work. Typed state carries the request and result; a router chooses the next path based on checked values, not on a free-form model promise.",
    "09-control": "Guardrails are executable checks at input, output, and action boundaries. A human approval decision is external state; no prompt can manufacture it.",
    "10-resilience": "A checkpoint remembers completed Crew work after interruption. It does not create exactly-once semantics for side effects, so a stable action ID and an idempotent sink remain necessary.",
    "11-observability": "Events reveal what ran and in what order. A small local trace is enough to diagnose a missing tool call or unexpected retry without logging the entire customer prompt.",
    "12-evaluation": "An evaluation case is a named input and a measurable check. Separate objective safety contracts from subjective answer quality, because prose can look good while a boundary is broken.",
    "13-project": "The interface passes a request into one application entry point. Memory enriches context, the Flow owns control, the Crew researches, and the action gate controls the only side effect.",
    "14-capstone": "A visible failure may originate in a different layer from the final answer. A reproducible test identifies the violated contract before a targeted repair is made.",
}

PRODUCTION_NOTES = {
    "00-verify": "Pin the model and embedding versions and test both on the actual network and laptop class. Record a fallback path before the event.",
    "01-python-to-llm": "Use the model for synthesis, not as a source of truth. Keep arithmetic and known business rules in deterministic code.",
    "02-agent-loop": "Set iteration, time, and cost limits for every run. Capture the reason a run stopped so timeout and success are not confused.",
    "03-tools": "Expose only needed tools, validate arguments inside Python, and limit permissions. Tool descriptions are part of the interface contract.",
    "04-mcp": "Treat an MCP server as a separate trust boundary: pin the server, inspect discovered tools, constrain filesystem/network access, and close connections reliably.",
    "05-knowledge": "Define document ownership, retention, and re-indexing rules. Evaluate retrieval relevance and source attribution separately from answer fluency.",
    "06-memory": "Define what may be retained, for how long, and how it is deleted. Test tenant isolation with negative cases, not just successful recall.",
    "07-crews": "Add a specialist only when its distinct role improves measurable quality. Each extra handoff adds latency and a chance to propagate a bad claim.",
    "08-flows": "Keep routing and retry counts in code, and make failure an explicit outcome. Persist only the state needed to resume safely.",
    "09-control": "Authorize side effects through the host application, store approval evidence, and use idempotency keys. Model output is never an authorization token.",
    "10-resilience": "Test interruption after each task and directly before/after every side effect. Restore from real checkpoints and make external actions replay-safe.",
    "11-observability": "Record correlation IDs, duration, and boundary outcomes while redacting customer data. Decide whether external trace export is permitted before enabling it.",
    "12-evaluation": "Run safety and contract cases in CI. Keep a small labeled set of grounded-answer examples for model or prompt changes.",
    "13-project": "The CLI is the workshop's minimal interface; an API or UI can call the same entry point later. Do not reimplement the Flow's approval logic in that interface.",
    "14-capstone": "Turn each discovered fault into a regression test with a named boundary. Recheck adjacent boundaries so the repair does not move the failure elsewhere.",
}

STEP_NOTES = {
    "00-verify": ["Inspect package/model configuration, then run an independent chat and embedding smoke test."],
    "01-python-to-llm": ["Run the deterministic rule with known inputs; note what it cannot infer.", "Call the CrewAI LLM on the same facts and mark any assertion unsupported by the prompt."],
    "02-agent-loop": ["Trace action, observation, and stop in plain Python first.", "Build a bounded CrewAI Agent and Task; inspect the final output as one run of the loop."],
    "03-tools": ["Test the pure ROI function and its invalid-input contract before involving the model.", "Wrap that function with CrewAI's @tool decorator and write a precise description.", "Give the agent only the needed tool, then distinguish the numeric tool result from the model's narrative."],
    "04-mcp": ["Configure a local stdio server process; this file is the client side.", "Discover the tool inside the adapter's connection lifetime, then attach it to the CrewAI agent."],
    "05-knowledge": ["Inspect the document search and explicit embedding configuration.", "Attach Knowledge sources to the Crew and demand source IDs and unknowns in the answer."],
    "06-memory": ["Create Memory and save two customers' facts in distinct scopes.", "Recall each scope independently and inspect the tree for isolation."],
    "07-crews": ["Define three CrewAI Agents with distinct roles, goals, and tool permissions.", "Connect three Tasks with explicit context and require a typed final report.", "Kick off the sequential Crew and inspect the typed DecisionReport, not just the final prose."],
    "08-flows": ["Instantiate typed Flow state and supply the request fields.", "Inspect report, retry count, and failure route after kickoff."],
    "09-control": ["Reject an invalid question and validate a deliberately sourced report.", "Exercise denied, approved, and replayed mock actions using the same ID."],
    "10-resilience": ["Create a checkpoint-enabled Crew with two tasks.", "Run normally or restore only from a real saved checkpoint path."],
    "11-observability": ["Register the local CrewAI event listener before kickoff.", "Read the JSONL event sequence and locate the first unexpected step."],
    "12-evaluation": ["Define independent cases and their plain-Python pass/fail conditions.", "Run every check and use a failing case to identify the broken boundary."],
    "13-project": ["Parse the CLI request and reject an approval flag without an action request.", "Run the same Flow used earlier; inspect report and action route separately."],
    "14-capstone": ["Load the seeded-fault examples and run the indicated checks.", "Change only the responsible layer, rerun the checks, and explain the regression prevented."],
}


def cells_from_script(source: str) -> list[dict[str, object]]:
    cells: list[dict[str, object]] = []
    kind = "code"
    lines: list[str] = []

    def flush() -> None:
        if not any(line.strip() for line in lines):
            return
        if kind == "markdown":
            rendered = [line[2:] if line.startswith("# ") else line[1:] if line.startswith("#") else line for line in lines]
            cells.append({"cell_type": "markdown", "metadata": {}, "source": rendered})
        else:
            cells.append({"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": lines.copy()})

    for line in source.splitlines(keepends=True):
        if line.startswith("# %% [markdown]"):
            flush()
            lines = []
            kind = "markdown"
        elif line.startswith("# %%"):
            flush()
            lines = []
            kind = "code"
        else:
            lines.append(line)
    flush()
    return cells


def main() -> None:
    for script in sorted((ROOT / "workshop").glob("[0-9][0-9]-*/*.py")):
        source_cells = cells_from_script(script.read_text(encoding="utf-8"))
        problem, concept, architecture, exercise, check = GUIDES[script.parent.name]
        folder = script.parent.name
        intro = [
            {"cell_type": "markdown", "metadata": {}, "source": [f"## Problem\n\n{problem}\n"]},
            {"cell_type": "markdown", "metadata": {}, "source": [
                f"## Concept\n\n{concept}\n\n"
                f"{CONCEPT_DETAILS[folder]}\n"
            ]},
            {"cell_type": "markdown", "metadata": {}, "source": [
                f"## Abstraction\n\n{architecture}. This is the smallest new layer introduced "
                "by this lesson; the earlier layers remain in place.\n"
            ]},
            {"cell_type": "markdown", "metadata": {}, "source": [
                f"## Architecture\n\n```text\n{ARCHITECTURES[folder]}\n```\n\n"
                "Follow the arrows while executing the cells. A tool result or validation failure "
                "is an observation, not an instruction that the model may bypass.\n"
            ]},
        ]
        cells = [source_cells[0], *intro]
        step = 0
        for cell in source_cells[1:]:
            if cell["cell_type"] == "code":
                notes = STEP_NOTES[folder]
                note = notes[min(step, len(notes) - 1)]
                step += 1
                cells.append({"cell_type": "markdown", "metadata": {}, "source": [
                    f"## Step {step} — {note.split(';')[0].rstrip('.')}\n\n{note}\n"
                ]})
            cells.append(cell)
        cells.extend([
            {"cell_type": "markdown", "metadata": {}, "source": [
                f"## Execution flow\n\n{architecture}. "
                "Read the printed result together with the task, selected tool, state, or trace. "
                "If the result differs, locate the first boundary where the observed value changed.\n"
            ]},
            {"cell_type": "markdown", "metadata": {}, "source": [
                f"## Failure mode to know about\n\n{FAILURES[folder]}\n"
            ]},
            {"cell_type": "markdown", "metadata": {}, "source": [
                f"## Production implication\n\n{PRODUCTION_NOTES[folder]}\n"
            ]},
            {"cell_type": "markdown", "metadata": {}, "source": [
                f"## Your turn\n\n{exercise}\n\n**Checkpoint:** {check}\n"
            ]},
        ])
        notebook = {
            "cells": cells,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
            "nbformat": 4,
            "nbformat_minor": 4,
        }
        target = script.with_suffix(".ipynb")
        target.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
