# CrewAI agentic harness workshop

This is the hands-on implementation of [the workshop plan](../plan.md). It follows the numbered-folder pattern of the supplied reference workshop: each folder has a runnable `1-topic.py` and a teaching `1-topic.ipynb` with the same code split into small cells. The Python files are the source for the notebooks; regenerate notebooks with `uv run python tools/generate_notebooks.py` from the repository root.

All agent, Crew, Flow, Knowledge, Memory, tool, MCP adapter, checkpoint, and event-listener examples use **CrewAI**. The reference repository supplies the teaching format, not its agent framework or finance-demo content.

Each numbered lesson is a topic folder with a runnable Python script and a matching notebook. The notebook follows the reference's instructional arc: **Problem → Concept → Abstraction → Architecture → Step-by-step code → Execution flow → Failure mode → Production implication → Your turn**. Architecture diagrams and concept notes are notebook-only; executable code stays synchronized with the paired script.

## Prerequisites

- `uv` installed at OS level.
- Python 3.12, installed automatically by `uv` if needed.
- Primary model path: Ollama and a tool-capable model such as `qwen3.5:4b`, plus `nomic-embed-text` for Knowledge and Memory. Confirm that this pair works on the actual workshop laptops before the event. A hosted model can replace the chat model, but the embedding provider must also be configured explicitly.
- Run commands from the repository root. A notebook kernel should also start with this root as its working directory.

## Windows setup (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1
ollama pull qwen3.5:4b
ollama pull nomic-embed-text
uv run python workshop\00-verify\1-verify_setup.py
```

The setup script uses native Windows Python 3.12 and verifies the local MCP
stdio subprocess without calling a model. You can also run its steps manually:

```powershell
uv sync --locked --python 3.12
Copy-Item .env.example .env
uv run python tools\verify_windows.py
```

Run `uv run python tools\check_prerequisites.py` after starting Ollama to check
the installed packages, embedded SQLite storage, endpoint, and downloaded models.

Do not reuse a `.venv` created by WSL. Windows environments contain
`.venv\Scripts\python.exe`; WSL environments contain Linux paths and may include
a `lib64` symbolic link that Windows cannot replace cleanly.

## macOS, Linux, or WSL setup

```bash
uv sync --locked --python 3.12
test -f .env || cp .env.example .env
ollama pull qwen3.5:4b
ollama pull nomic-embed-text
uv run python workshop/00-verify/1-verify_setup.py
```

`uv sync` creates a platform-specific `.venv`. The `.env` file holds local model settings and is ignored by Git. The setup check reports a missing model service before the first lab. On a restricted network, pre-download dependencies and models before the teaching day.

The cross-platform check is `uv run python tools/check_prerequisites.py`; add
`--offline` to skip the model-service probe while verifying packages and local storage.

For an approved OpenAI fallback, set `WORKSHOP_MODEL=openai/<model-id>`, `WORKSHOP_EMBEDDING_PROVIDER=openai`, `WORKSHOP_EMBEDDING_MODEL=text-embedding-3-small`, and `OPENAI_API_KEY` in `.env`. The code never changes provider implicitly. Test the exact model's tool calling and structured-output behavior before using it in class.

Run any pair like this:

```bash
uv run python workshop/03-tools/1-custom_tools.py
uv run jupyter lab workshop/03-tools/1-custom_tools.ipynb
```

To demonstrate retained customer context in the final project, run it once
with `--remember "Customer requires private VPC deployment"`, then run it
again with the same `--customer` and no `--remember`. The memory lookup is
scoped to that customer.

For notebooks, select the project's `.venv` Python kernel. The notebooks are deliberately saved without execution outputs: participants produce their own trace and result.

## Reading order

| Folder | What changes | Core checkpoint |
| --- | --- | --- |
| `00-verify` | Environment | CrewAI imports and model responds |
| `01-python-to-llm` | Plain Python → CrewAI LLM call | Identify an unsupported claim |
| `02-agent-loop` | LLM call → bounded Agent | Explain action, observation, stop |
| `03-tools` | Agent gains a typed tool | Invalid input is rejected |
| `04-mcp` | Same capability through a local MCP server | Server tool discovered by CrewAI |
| `05-knowledge` | Agent grounds answer in documents | Answer cites source IDs |
| `06-memory` | Customer constraint survives a run | Cross-customer scope stays separate |
| `07-crews` | Researcher, Analyst, Critic collaborate | Structured recommendation |
| `08-flows` | Flow controls Crew, state, and retry | Success or evidence-gap route |
| `09-control` | Guardrail and action approval | Mock email stays blocked until approved |
| `10-resilience` | Crew checkpoint | Interrupted work can resume |
| `11-observability` | CrewAI event listener | Run events in local trace |
| `12-evaluation` | Behavioral checks | Objective checks pass |
| `13-project` | End-to-end assistant | Report and approval route work together |
| `14-capstone` | Eight seeded harness faults | Diagnose and repair one or two faults |

The sample company is fictional. Its documents are in `workshop/data/`. The external research tool returns a fixed fixture, and the email action only writes a local record under `workshop/.workshop-data/`. No lesson sends real mail or requires live web search. [Guided exercises](labs/lab-exercises.md), participant pre-work, the instructor runbook, slide source, one-page recap, and production-readiness checklist are included in this folder.

The reference project's React/FastAPI finance portal is not copied into this different capstone. This proposal's core project is a source-backed enterprise AI decision assistant; its CLI is the runnable interface, and the same application entry point can later be called from an approved API or UI.

## Five questions for every topic

1. What failure in the previous stage does this solve?
2. What is the new abstraction?
3. What is the smallest code change that uses it?
4. What happens inside the model/tool/Flow execution path?
5. When would a simpler design be enough?

## Instructor runbook

Use the proposal's 9:00–5:30 schedule in [plan.md](../plan.md). The paired files support a short explanation, a code edit, and inspection of a concrete result. Keep a clean repository copy available so a pair can move to the next numbered folder if a model call is slow. Assign one or two of the eight capstone faults per pair; debrief all faults together.

Before the event, run every script and notebook with the pinned environment and selected model on a target-class laptop. Verify Knowledge and Memory embeddings separately, the local MCP subprocess, Flow branching, checkpoint restore, and the mock email idempotency check. CrewAI tracing export is disabled by default; the local event trace is the required classroom path.

## Verification without a model

```bash
uv run pytest -q
```

The checks cover the deterministic contracts and lesson file parity. Live model output remains variable and needs the instructor rehearsal described above.

## Technical references

- [CrewAI production architecture](https://docs.crewai.com/v1.15.22/en/concepts/production-architecture)
- [CrewAI Agents](https://docs.crewai.com/v1.15.22/en/concepts/agents), [Tasks](https://docs.crewai.com/v1.15.22/en/concepts/tasks), and [Flows](https://docs.crewai.com/v1.15.22/en/concepts/flows)
- [CrewAI Knowledge](https://docs.crewai.com/v1.15.22/en/concepts/knowledge) and [Memory](https://docs.crewai.com/v1.15.22/en/concepts/memory)
- [CrewAI MCP adapter](https://docs.crewai.com/v1.15.22/en/mcp/overview), [checkpointing](https://docs.crewai.com/v1.15.22/en/concepts/checkpointing), and [event listeners](https://docs.crewai.com/v1.15.22/en/concepts/event-listener)
