# %% [markdown]
# # 22 — Package the advanced track with Podman
# The Compose file starts PostgreSQL, Redis, the API, and Streamlit. Ollama
# runs on the host; Langfuse is an explicitly configured separate endpoint.

# %%
import shutil
import sys
from pathlib import Path

here = Path(__file__).resolve() if "__file__" in globals() else Path.cwd() / "lesson.py"
sys.path.insert(0, str(next(p for p in here.parents if (p / "pyproject.toml").exists())))

from workshop.common import ROOT

print("Podman installed:", bool(shutil.which("podman")))
print("Compose file exists:", (ROOT / "compose.yaml").is_file())
print("Containerfile exists:", (ROOT / "Containerfile").is_file())

# %% [markdown]
# ## Start services after setting credentials in .env
# Run `podman compose up --build` from the repository root. Verify /ready and
# the UI at localhost:8501. `podman compose` needs a Compose provider installed.

# %%
print("API readiness URL: http://localhost:8000/ready")
print("Streamlit URL: http://localhost:8501")
