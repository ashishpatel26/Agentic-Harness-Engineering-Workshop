# %% [markdown]
# # 17 — CrewAI Knowledge and a separate LanceDB retriever
# Knowledge's built-in store is not LanceDB. This adapter indexes the same
# fictional documents separately and returns source IDs for inspection.

# %%
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

from workshop.retrieval import index_documents, search_index
from workshop.tools import DOCUMENTS

print("Available source IDs:", DOCUMENTS)

# %% [markdown]
# ## Index and query with local Ollama embeddings
# Requires the configured embedding model and a running Ollama service.

# %%
if os.getenv("WORKSHOP_RUN_LIVE_DEMOS") == "true":
    print("Indexed:", index_documents())
    print("Results:", search_index("private deployment and deletion guarantee"))
else:
    print("Set WORKSHOP_RUN_LIVE_DEMOS=true to build and query the LanceDB index.")
