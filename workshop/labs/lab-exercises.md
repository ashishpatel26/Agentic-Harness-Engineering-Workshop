# Guided lab exercises and reference solutions

The numbered notebooks contain complete runnable examples so a participant can rejoin at any stage. For a hands-on exercise, copy the named code cell into a new cell, make the requested change, and run it. The matching `.py` file and shared module are the reference implementation; the notebook's **Checkpoint** states what to verify. Keep the original cell so the next topic still runs.

| Topic | Edit in your copied cell | Inspect or assert | Reference implementation |
| --- | --- | --- | --- |
| 00 Setup | Change the smoke-test prompt to ask for one word | Both chat and embedding checks still respond | `00-verify/1-verify_setup.py` |
| 01 Python → LLM | Change the annual cost to exceed the benefit | Compare deterministic and model answers; label assumptions | `01-python-to-llm/1-first_model_call.py` |
| 02 Agent loop | Lower `max_iter` from 3 to 1 | Explain how the stop bound changes the run | `02-agent-loop/1-first_agent.py` |
| 03 Tools | Call the pure ROI function with zero and negative cost | Both invalid cases raise `ValueError` | `workshop/tools.py` |
| 04 MCP | Print the MCP adapter's discovered tool names | `annual_roi` is available while the context manager is open | `04-mcp/1-local_mcp_tool.py` |
| 05 Knowledge | Ask which deletion guarantee is verified | The answer says none is verified and names `security.md` | `05-knowledge/1-grounded_answer.py` |
| 06 Memory | Add a third customer with a different preference | The third customer's recall excludes A and B | `workshop/memory.py` |
| 07 Crew | Change the Critic's task to demand an explicit unknown | The final report places the gap under risk or next step | `workshop/crew.py` |
| 08 Flow | Feed the report validator a one-source result | Route to insufficient evidence after at most two attempts | `workshop/decision_flow.py` and `tests/test_decision_flow.py` |
| 09 Control | Try an unknown citation and an unapproved action | Citation rejected; no mock action record | `workshop/control.py` |
| 10 Resilience | Interrupt after task one and resume with the saved file | Task one does not need to be rerun manually | `10-resilience/1-checkpoint_resume.py` |
| 11 Observability | Filter the JSONL trace for tool events | Explain the tool's place between Crew start and finish | `workshop/observability.py` |
| 12 Evaluation | Add a case with an unknown source ID | The new case fails before the source is corrected | `12-evaluation/1-evaluate_harness.py` |
| 13 Project | Store a constraint with `--remember`, then rerun without it | The next run recalls it for the same customer | `workshop/app.py` |
| 14 Capstone | Fix one or two assigned faults | The matching failure checks turn to PASS | `14-capstone/INSTRUCTOR.md` (instructor only) |

For exercises that call a model, compare the observable contract rather than exact prose. A model can phrase the right answer differently. The objective checks in `tests/` cover the contracts that must not vary.
