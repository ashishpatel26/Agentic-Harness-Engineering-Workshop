"""Pure checks for the cross-platform prerequisite checker."""

import pytest

from tools.check_prerequisites import installed_model_names, is_model_present, ollama_tags_url


def test_ollama_tags_uses_configured_host() -> None:
    assert ollama_tags_url("http://localhost:11434/v1") == "http://localhost:11434/api/tags"
    assert ollama_tags_url("https://models.example.test/api/embeddings") == "https://models.example.test/api/tags"
    with pytest.raises(ValueError):
        ollama_tags_url("localhost:11434")


def test_model_list_handles_both_ollama_name_fields() -> None:
    names = installed_model_names({"models": [{"name": "qwen2.5:7b"}, {"model": "nomic-embed-text"}]})
    assert names == {"qwen2.5:7b", "nomic-embed-text"}
    assert is_model_present("qwen2.5:7b", names)
    assert is_model_present("qwen2.5:7b", {"library/qwen2.5:7b"})
    assert not is_model_present("missing:latest", names)
    with pytest.raises(ValueError):
        installed_model_names({"models": "not a list"})
