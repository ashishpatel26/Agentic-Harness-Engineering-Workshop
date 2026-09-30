# %% [markdown]
# # 16 — A UI that does not own agent logic
# Streamlit sends validated requests to FastAPI; the application and Flow remain
# on the server. The Streamlit app lives in workshop/ui.py.

# %%
import os
import sys
from pathlib import Path

here = Path(__file__).resolve() if "__file__" in globals() else Path.cwd() / "lesson.py"
sys.path.insert(0, str(next(p for p in here.parents if (p / "pyproject.toml").exists())))

from workshop.api import api
from workshop.ui_contract import decision_payload

print("Payload:", decision_payload("customer-a", "Should Northstar AI pilot Meridian AI?"))
print("UI command: uv run --extra advanced streamlit run workshop/ui.py")
print("API URL:", os.getenv("WORKSHOP_API_URL", "http://localhost:8000"))
