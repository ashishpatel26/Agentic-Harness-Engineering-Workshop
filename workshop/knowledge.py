"""CrewAI Knowledge example, with a separately configured local embedder."""

from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

from workshop.common import DATA, embedder_config
from workshop.tools import DOCUMENTS


def sample_knowledge() -> tuple[list[StringKnowledgeSource], dict[str, object]]:
    sources = [
        StringKnowledgeSource(
            content=f"Source ID: {name}\n{(DATA / name).read_text(encoding='utf-8')}"
        )
        for name in DOCUMENTS
    ]
    return sources, embedder_config()
