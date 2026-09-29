# %% [markdown]
# # 06 — Memory across runs
# Flow state belongs to one run. Memory can be recalled in a later run.
# Explicit scopes keep Customer A's preference out of Customer B's context.

# %%
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

import workshop  # configure project-local CrewAI storage
from crewai import Memory

from workshop.common import embedder_config
from workshop.memory import customer_scope

memory = Memory(embedder=embedder_config())
memory.remember(
    "Customer A requires private VPC deployment.",
    scope=customer_scope("customer-a"),
    source="customer:customer-a",
)
memory.remember(
    "Customer B prefers a managed SaaS pilot.",
    scope=customer_scope("customer-b"),
    source="customer:customer-b",
)

# %% [markdown]
# ## Recall from a customer scope
# Inspect both results. A result from the wrong customer indicates a serious
# isolation problem, not just a weak answer.

# %%
for customer in ("customer-a", "customer-b"):
    matches = memory.recall("deployment preference", scope=customer_scope(customer), limit=3)
    print(customer, [match.record.content for match in matches])
print("Memory tree:\n", memory.tree())

# %% [markdown]
# ## Bonus scenario — team meeting notes
# Scopes work for any grouping, here teams (inspired by CrewAI's *Meeting Assistant* example).
# Each team's action item stays in its own scope.

# %%
memory.remember("Design team: send the new logo files to marketing by Friday.", scope="/team/design")
memory.remember("Data team: retrain the churn model after the schema change.", scope="/team/data")
for team in ("design", "data"):
    matches = memory.recall("what is the action item?", scope=f"/team/{team}", limit=2)
    print(team, [match.record.content for match in matches])
