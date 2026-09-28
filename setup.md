# Workshop technology stack and setup plan

This is the source of truth for the workshop's **core** and **advanced** tracks. The core track remains local-first. Advanced modules and lesson pairs are implemented, but a live end-to-end run still needs Ollama, PostgreSQL, Redis, and (optionally) a Langfuse server.

## Stack at a glance

| Layer | Target technology | Current state | Teaching role |
| --- | --- | --- | --- |
| Agent framework | CrewAI | Implemented | Agents, tasks, crews, and tools |
| Workflow | CrewAI Flows | Implemented | Explicit state, branching, retries, and approval gates |
| LLM and embeddings | Ollama + local open models | Implemented | Default model path; no paid API required |
| API | FastAPI | Implemented; HTTP smoke tested | Expose the existing application boundary over HTTP |
| UI | Streamlit | Implemented; live browser untested | Human-facing form, result, citations, and mock approval interaction |
| RAG | CrewAI Knowledge + separate LanceDB retrieval adapter | Implemented; LanceDB tested with synthetic vectors | Ground answers in source documents; see the storage distinction below |
| Database | PostgreSQL | Adapter and schema implemented; live server untested | Durable application runs and mock approvals |
| Memory | CrewAI Memory | Implemented | Scoped recall; its default local storage is LanceDB |
| Cache | Redis | Adapter implemented; live server untested | Disposable ROI cache, never approval state |
| Tools | Typed Python custom tools | Implemented | Deterministic capabilities with validated inputs |
| External tools | MCP | Implemented | Discover and call an external tool through a local MCP server |
| Guardrails | NeMo Guardrails with Ollama + CrewAI task checks + Python/Pydantic | Integrated; NeMo config constructed; live model checks untested | Screen input/output and enforce action policy outside the model |
| Observability | Langfuse | Opt-in integration implemented; live server untested | Trace CrewAI spans; local JSONL trace remains the offline fallback |
| Evaluation | Ragas | Local evaluator implemented; live score untested | Factual score with Ollama; deterministic checks remain first |
| Testing | pytest; `crewai test` where supported | pytest implemented; CLI path conditional | Fast offline contract tests plus optional model-judged crew runs |
| Deployment | Podman + Compose | Manifest validated; image build untested | Containerized API, UI, PostgreSQL, and Redis |
| Authentication | Keycloak | **Not part of this workshop** | Name as a production extension only; no install or lesson dependency |
| Workflow resilience | CrewAI Checkpointing | Implemented as a lesson; deeper recovery tests planned | Resume work without treating a checkpoint as exactly-once side-effect protection |

## Important compatibility decisions

1. **Knowledge and Memory are different stores.** CrewAI Knowledge uses ChromaDB by default, while CrewAI Memory defaults to **LanceDB**. [`workshop/retrieval.py`](workshop/retrieval.py) is a *separate* LanceDB document retriever, not a replacement for built-in Knowledge. Lesson 17 demonstrates it; `WORKSHOP_LANCEDB_RAG_ENABLED=true` attaches its tool to the research Crew after building the index. See [CrewAI Knowledge](https://docs.crewai.com/v1.15.22/en/concepts/knowledge) and [Memory](https://docs.crewai.com/v1.15.22/en/concepts/memory).
2. **`crewai test` is not the local-only test gate.** CrewAI's pinned-version documentation says its CLI testing evaluator supports OpenAI and defaults to `gpt-4o-mini`. Keep `uv run pytest -q` mandatory and offline. Add `crewai test` only as an explicitly opt-in hosted-evaluator exercise after confirming project compatibility and credentials; do not run it automatically for Ollama learners. See [CrewAI Testing](https://docs.crewai.com/v1.15.22/en/concepts/testing).
3. **Guardrails have three jobs.** [NeMo Guardrails](https://docs.nvidia.com/nemo/guardrails/latest/run-guardrailed-inference/using-python-apis/check-messages) screens question and report text using the **same Ollama chat model**; a CrewAI task guardrail can reject bad task output and retry it; Python/Pydantic and PostgreSQL enforce approval and idempotency. Set `WORKSHOP_NEMO_ENABLED=true` only after testing false positives, misses, latency, and your local model. NeMo is not a guarantee against prompt injection. See [NeMo Ollama configuration](https://docs.nvidia.com/nemo/guardrails/configure-guardrails/configuration-reference) and [CrewAI task guardrails](https://docs.crewai.com/v1.15.22/en/concepts/tasks).
4. **Langfuse is a deliberate opt-in.** Lesson 11's prompt-free local event trace remains the offline path. [`workshop/langfuse_tracing.py`](workshop/langfuse_tracing.py) uses Langfuse's [CrewAI OpenInference integration](https://langfuse.com/integrations/frameworks/crewai) only after `WORKSHOP_LANGFUSE_ENABLED=true` and valid project credentials. Remote spans can include prompts and customer context. The Podman file does **not** self-host Langfuse; configure an approved external or separately self-hosted endpoint.
5. **Ragas metrics are not safety policy.** [`workshop/ragas_eval.py`](workshop/ragas_eval.py) uses Ragas FactualCorrectness and the Ollama OpenAI-compatible endpoint. It is a model-judged score, not an offline or deterministic gate. Retain pytest assertions for citations, isolation, and approval. See [Ragas local-model guidance](https://docs.ragas.io/en/stable/howtos/llm-adapters/).
6. **Checkpointing is not a transaction.** The existing checkpoint lesson can resume Crew work, but PostgreSQL must own durable action/approval records and idempotency keys. Redis must not become the only copy of a decision or approval. See [CrewAI Checkpointing](https://docs.crewai.com/v1.15.22/en/concepts/checkpointing).

## Learner setup, in two tracks

### Core track: lessons 00–14

Install OS-level [uv](https://docs.astral.sh/uv/getting-started/installation/) and [Ollama](https://ollama.com/download). The project uses Python 3.12. From the repository root:

```bash
uv sync --locked --python 3.12
ollama pull qwen3.5:4b
ollama pull nomic-embed-text
uv run python tools/check_prerequisites.py --offline
uv run python tools/check_prerequisites.py
uv run pytest -q
```

Start the Ollama service before the full check. Follow [README.md](README.md#start-here) for Windows/WSL-specific instructions and the `.env` setup. PostgreSQL, Redis, Podman, Langfuse, and Keycloak are **not required** for the core track.

The default local model configuration belongs in the ignored `.env` file (copy from [`.env.example`](.env.example)), not in a notebook or a hard-coded Python constant:

```dotenv
WORKSHOP_MODEL=ollama/qwen3.5:4b
WORKSHOP_MODEL_BASE_URL=http://localhost:11434
WORKSHOP_EMBEDDING_PROVIDER=ollama
WORKSHOP_EMBEDDING_MODEL=nomic-embed-text
WORKSHOP_OLLAMA_EMBED_URL=http://localhost:11434/api/embeddings
CREWAI_TRACING_ENABLED=false
```

`qwen3.5:4b` is the CrewAI and NeMo chat model; `nomic-embed-text` is the Knowledge/Memory/LanceDB embedding model. NeMo reads the `WORKSHOP_MODEL` and `WORKSHOP_MODEL_BASE_URL` values and appends `/v1` for Ollama's OpenAI-compatible API. The full prerequisite check confirms the service and both model downloads. NeMo stays off until `WORKSHOP_NEMO_ENABLED=true`.

The LanceDB retrieval tool is also opt-in: set `WORKSHOP_LANCEDB_RAG_ENABLED=true` to index the fictional documents and expose the tool to the Crew. Redis is used only by the ROI tool and falls back to the same Python calculation if the cache is absent.

### Advanced track: end-to-end application

Install the optional dependencies and check the host tooling:

```bash
uv sync --locked --extra advanced --python 3.12
uv run --extra advanced python tools/check_prerequisites.py --offline --advanced
```

Copy `.env.example` to ignored `.env`. Set unique values for `WORKSHOP_API_TOKEN`, `WORKSHOP_APPROVAL_TOKEN`, and `WORKSHOP_POSTGRES_PASSWORD`; do not reuse these example names as credentials. With Ollama running on the host, start the services:

```bash
uv run --extra advanced podman compose up --build
curl http://localhost:8000/ready
```

The API is bound to `http://localhost:8000` and the UI to `http://localhost:8501`. In containers, the API reaches host Ollama through `host.containers.internal`. The full advanced checker needs **host-reachable** PostgreSQL and Redis URLs; Compose supplies those URLs only inside the API container, so use `/ready` for the containerized service check. For a host-native alternative, set those URLs and run `uv run --extra advanced uvicorn workshop.api:api --host 127.0.0.1 --port 8000` plus `uv run --extra advanced streamlit run workshop/ui.py`. Keep credentials in ignored `.env` files or a secrets mechanism. Keycloak is not used.

Podman Compose uses an external provider; the advanced uv extra includes `podman-compose`. The manifest was parsed successfully, but image build and live multi-service startup have not yet been verified here. Langfuse is not included in this Compose stack.

## Target architecture

```text
Streamlit UI ──▶ FastAPI ──▶ workshop.app.run_assistant()
                             │
                             ├── NeMo input/output checks (opt-in)
                             ├── CrewAI Flow ──▶ research Crew + tools + MCP
                             │                    ├── built-in Knowledge
                             │                    └── LanceDB tool (opt-in)
                             ├── scoped CrewAI Memory (local LanceDB)
                             └── PostgreSQL (runs and mock approvals)

Separate lessons: LanceDB document retrieval, Redis ROI cache,
Ragas/Ollama factual score, and Langfuse traces (opt-in).
Podman packages API/UI/PostgreSQL/Redis; Ollama runs on the host.
```

The existing `workshop/app.py` remains the single CrewAI application boundary. Streamlit calls FastAPI; FastAPI calls `run_assistant` with `approved=False`. A separate instructor-token endpoint records a mock approval atomically in PostgreSQL; it never sends mail. The shared workshop token is **not** per-customer authentication. Do not expose this demo beyond localhost or use real customer data without adding real identity and authorization.

## Implementation map

| Area | Implemented and verified | Live check still needed |
| --- | --- | --- |
| API/UI | `workshop/api.py`, `workshop/ui.py`, and lessons 15–16; HTTP contract smoke passes | Browser run with Ollama |
| Retrieval | `workshop/retrieval.py` and lesson 17; LanceDB query tested with synthetic vectors | Real Ollama embeddings and relevance |
| State/cache | `workshop/persistence.py`, `workshop/cache.py`, and lesson 18 | PostgreSQL create/approve/replay/restart; Redis loss |
| Guardrails | `workshop/nemo_guardrails.py` and lesson 19; config constructs | Ollama judgment quality, false positives, latency |
| Trace/evaluation | `workshop/langfuse_tracing.py`, `workshop/ragas_eval.py`, and lessons 20–21 | Approved Langfuse project and live Ragas score |
| Deployment | `Containerfile`, `compose.yaml`, lesson 22, and advanced preflight; Compose config parses | Image build and multi-service startup |

Each advanced topic has a script and a matching generated notebook with **Problem → Concept → Abstraction → Architecture → Steps → Failure mode → Production implication → Your turn**. Regenerate from scripts with `uv run --extra advanced python tools/generate_notebooks.py`.

## Remaining acceptance gates

1. Run a complete Ollama session from CLI, API, and UI on a target-class laptop. Confirm both models, then explicitly enable and inspect NeMo checks.
2. Start PostgreSQL and Redis under Podman, exercise create/approve/replay, restart services, and confirm approvals persist while Redis loss leaves results unchanged.
3. Build a LanceDB index with real Ollama embeddings, score a versioned Ragas fixture, and inspect an approved Langfuse trace for sensitive content.
4. Replace shared demo tokens with actual identity and authorization, add formal database migrations, and pin container image digests before any non-demo deployment.

No real email or Keycloak integration is included.
