# %% [markdown]
# # 18 — Durable state versus disposable cache
# PostgreSQL records runs and approvals. Redis caches only a pure ROI number;
# losing the cache cannot change authorization or the result.

# %%
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

from workshop.cache import cached_annual_roi
from workshop.persistence import configured_store

print("ROI scenario:", cached_annual_roi(45_000, 30_000))
print("PostgreSQL configured:", configured_store() is not None)

# %% [markdown]
# ## Check the database only in a configured advanced environment
# This does not create a run or send an email.

# %%
if os.getenv("WORKSHOP_RUN_LIVE_DEMOS") == "true":
    store = configured_store()
    if store is None:
        raise RuntimeError("Set WORKSHOP_DATABASE_URL before running the live state lab")
    store.initialize()
    print("PostgreSQL ready:", store.ping())
else:
    print("Set WORKSHOP_RUN_LIVE_DEMOS=true to check PostgreSQL connectivity.")
