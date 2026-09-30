"""Hands-on CrewAI workshop lessons and reusable example components.

CrewAI creates its local storage directory during import. Set it before any
lesson imports CrewAI so runs stay inside this project and work in sandboxes.
"""

import asyncio
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_storage = Path(__file__).resolve().parent / ".workshop-data" / "crewai"
_storage.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("CREWAI_STORAGE_DIR", str(_storage))


def _make_crewai_work_in_jupyter() -> None:
    """Three small fixes so the lesson code runs unchanged inside a notebook.

    Scripts have no running event loop and never call this.
    """
    from crewai import Crew

    # 1. CrewAI refuses a synchronous Crew.kickoff() inside a running loop
    #    ("invoked synchronously from within a running event loop"). Run the
    #    same blocking call on a worker thread, which has no loop.
    blocking_kickoff = Crew.kickoff

    def kickoff_in_thread(self, *args, **kwargs):
        with ThreadPoolExecutor(max_workers=1) as pool:
            return pool.submit(blocking_kickoff, self, *args, **kwargs).result()

    Crew.kickoff = kickoff_in_thread

    # 2. The MCP lesson starts a stdio server subprocess. On Windows ipykernel
    #    selects a loop that cannot, so new loops get the default one.
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # 3. MCP hands sys.stderr to that subprocess, but the kernel's stderr has
    #    no file handle ("UnsupportedOperation: fileno"); lend it the original.
    try:
        sys.stderr.fileno()
    except (AttributeError, OSError, ValueError):
        if sys.__stderr__ is not None:
            sys.stderr.fileno = sys.__stderr__.fileno


try:
    asyncio.get_running_loop()
except RuntimeError:
    pass
else:
    _make_crewai_work_in_jupyter()
