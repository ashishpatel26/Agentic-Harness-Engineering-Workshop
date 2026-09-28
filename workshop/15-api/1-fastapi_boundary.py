# %% [markdown]
# # 15 — A typed HTTP boundary
# FastAPI accepts a validated request and calls the same application entry point
# as the CLI. A public request never supplies its own approval.

# %%
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] if "__file__" in globals() else Path.cwd()))

from fastapi.testclient import TestClient
from workshop.api import api

client = TestClient(api)
print("Health:", client.get("/health").json())
print("Unauthenticated request status:", client.post("/decisions", json={
    "question": "Should Northstar AI pilot Meridian AI?", "customer_id": "customer-a"
}).status_code)

# %% [markdown]
# ## Run with a real model only when the instructor has configured it
# Set WORKSHOP_API_TOKEN and Ollama first. This call may take time.

# %%
if os.getenv("WORKSHOP_RUN_LIVE_DEMOS") == "true":
    token = os.environ["WORKSHOP_API_TOKEN"]
    response = client.post("/decisions", headers={"X-Workshop-API-Token": token}, json={
        "question": "Should Northstar AI pilot Meridian AI?", "customer_id": "customer-a"
    })
    print(response.status_code, response.json())
else:
    print("Set WORKSHOP_RUN_LIVE_DEMOS=true to call the local model through the API.")
