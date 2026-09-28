"""Hands-on CrewAI workshop lessons and reusable example components.

CrewAI creates its local storage directory during import. Set it before any
lesson imports CrewAI so runs stay inside this project and work in sandboxes.
"""

import os
from pathlib import Path

_storage = Path(__file__).resolve().parent / ".workshop-data" / "crewai"
_storage.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("CREWAI_STORAGE_DIR", str(_storage))
