"""A small local CrewAI event trace for the classroom."""

import json
from datetime import datetime, timezone

from crewai.events import (
    BaseEventListener,
    CrewKickoffCompletedEvent,
    CrewKickoffStartedEvent,
    LLMCallCompletedEvent,
    ToolUsageFinishedEvent,
)

from workshop.common import ensure_runtime


class LocalTrace(BaseEventListener):
    """Record event kinds and times without storing prompts or customer data."""

    def setup_listeners(self, event_bus):
        def record(_source, event):
            path = ensure_runtime() / "trace.jsonl"
            payload = {"time": datetime.now(timezone.utc).isoformat(), "event": type(event).__name__}
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload) + "\n")

        for event_type in (
            CrewKickoffStartedEvent,
            CrewKickoffCompletedEvent,
            LLMCallCompletedEvent,
            ToolUsageFinishedEvent,
        ):
            event_bus.on(event_type)(record)
