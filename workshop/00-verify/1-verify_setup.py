# %% [markdown]
# # 00 — Verify the workshop environment
# Run this before the first lab. It checks imports and makes one short model
# call. Knowledge and Memory need a second embedding model configured later.

# %%
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

import workshop  # configure project-local CrewAI storage before importing CrewAI
import crewai
from crewai.rag.embeddings.factory import build_embedder

from workshop.common import embedder_config, model

print("CrewAI:", crewai.__version__)
print("Embedding provider:", embedder_config()["provider"])
print("Model response:", model().call("Reply with exactly: workshop ready"))
embedding = build_embedder(embedder_config())(["workshop ready"])
print("Embedding dimensions:", len(embedding[0]))
