"""Check workshop tools, Python packages, local storage, and model readiness.

Run after ``uv sync --locked`` with ``uv run python tools/check_prerequisites.py``.
The default check contacts only the configured Ollama endpoint. Use --offline
when a model service is intentionally unavailable.
"""

from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = (
    "crewai",
    "crewai-tools",
    "mcp",
    "chromadb",
    "ollama",
    "jupyterlab",
    "ipykernel",
    "nbformat",
    "pytest",
)
ADVANCED_PACKAGES = (
    "fastapi", "uvicorn", "httpx", "streamlit", "psycopg", "redis",
    "lancedb", "nemoguardrails", "langfuse", "ragas",
    "openinference-instrumentation-crewai", "podman-compose",
)


def check_advanced(*, offline: bool) -> bool:
    """Return True if an advanced-track required check failed."""
    failed = False
    print("\nAdvanced-track prerequisites\n")
    for package in ADVANCED_PACKAGES:
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            print_check(package, "FAIL", "Install with uv sync --locked --extra advanced")
            failed = True
        else:
            print_check(package, "PASS", version)

    podman = shutil.which("podman")
    print_check("Podman", "PASS" if podman else "FAIL", podman or "Not on PATH")
    failed |= not bool(podman)
    if podman:
        try:
            result = subprocess.run(
                [podman, "compose", "version"], capture_output=True, text=True,
                check=False, timeout=10,
            )
            print_check("Compose provider", "PASS" if result.returncode == 0 else "FAIL",
                        result.stdout.strip().splitlines()[-1] if result.stdout.strip()
                        else result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "Unavailable")
            failed |= result.returncode != 0
        except (OSError, subprocess.TimeoutExpired) as error:
            print_check("Compose provider", "FAIL", str(error))
            failed = True

    if offline:
        print_check("PostgreSQL", "SKIP", "Offline mode")
        print_check("Redis", "SKIP", "Offline mode")
        print_check("Langfuse", "SKIP", "Offline mode")
        return failed

    dsn = os.getenv("WORKSHOP_DATABASE_URL", "").strip()
    if not dsn:
        print_check("PostgreSQL", "FAIL", "Set WORKSHOP_DATABASE_URL")
        failed = True
    else:
        try:
            from workshop.persistence import PostgresRunStore
            ok = PostgresRunStore(dsn).ping()
            print_check("PostgreSQL", "PASS" if ok else "FAIL", "SELECT 1")
            failed |= not ok
        except Exception as error:
            print_check("PostgreSQL", "FAIL", str(error))
            failed = True

    redis_url = os.getenv("WORKSHOP_REDIS_URL", "").strip()
    if not redis_url:
        print_check("Redis", "FAIL", "Set WORKSHOP_REDIS_URL")
        failed = True
    else:
        try:
            import redis
            ok = bool(redis.Redis.from_url(redis_url, socket_connect_timeout=2, socket_timeout=2).ping())
            print_check("Redis", "PASS" if ok else "FAIL", "PING")
            failed |= not ok
        except Exception as error:
            print_check("Redis", "FAIL", str(error))
            failed = True

    if os.getenv("WORKSHOP_LANGFUSE_ENABLED", "false").lower() == "true":
        try:
            from langfuse import get_client
            ok = bool(get_client().auth_check())
            print_check("Langfuse", "PASS" if ok else "FAIL", "Project authentication")
            failed |= not ok
        except Exception as error:
            print_check("Langfuse", "FAIL", str(error))
            failed = True
    else:
        print_check("Langfuse", "SKIP", "Remote tracing disabled")
    return failed


def ollama_tags_url(configured_url: str) -> str:
    """Use the same host as the configured model URL for Ollama's tag API."""
    parsed = urlsplit(configured_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Ollama URL must start with http:// or https:// and include a host")
    return urlunsplit((parsed.scheme, parsed.netloc, "/api/tags", "", ""))


def installed_model_names(payload: object) -> set[str]:
    """Extract names from Ollama's /api/tags response without trusting shape."""
    if not isinstance(payload, dict) or not isinstance(payload.get("models"), list):
        raise ValueError("Ollama returned an unexpected model-list response")
    return {
        name
        for model in payload["models"]
        if isinstance(model, dict)
        for name in (model.get("name"), model.get("model"))
        if isinstance(name, str)
    }


def is_model_present(requested: str, available: set[str]) -> bool:
    return requested in available or any(name.endswith("/" + requested) for name in available)


def print_check(label: str, status: str, detail: str) -> None:
    print(f"{status:>7}  {label:<22} {detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="Skip the model-service connection check")
    parser.add_argument("--advanced", action="store_true", help="Also check the advanced API/UI and service stack")
    args = parser.parse_args()

    try:
        from dotenv import load_dotenv

        load_dotenv(ROOT / ".env")
    except ImportError:
        pass  # The package check below will explain an unsynced environment.

    failed = False
    print("Workshop prerequisite check\n")

    python_ok = sys.version_info[:2] == (3, 12)
    print_check("Python", "PASS" if python_ok else "FAIL", f"{sys.version.split()[0]} at {sys.executable}; use 3.12")
    failed |= not python_ok

    uv_path = shutil.which("uv")
    if uv_path:
        result = subprocess.run([uv_path, "--version"], capture_output=True, text=True, check=False, timeout=5)
        uv_ok = result.returncode == 0
        print_check("uv", "PASS" if uv_ok else "FAIL", result.stdout.strip() or uv_path)
    else:
        uv_ok = False
        print_check("uv", "FAIL", "Not found on PATH")
    failed |= not uv_ok

    missing = []
    for package in PACKAGES:
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            missing.append(package)
            print_check(package, "FAIL", "Not installed in this Python environment")
        else:
            print_check(package, "PASS", version)
    failed |= bool(missing)

    env_file = ROOT / ".env"
    print_check(".env", "PASS" if env_file.is_file() else "WARN", "Present" if env_file.is_file() else "Missing; copy .env.example for explicit settings")

    try:
        connection = sqlite3.connect(":memory:")
        connection.execute("SELECT 1").fetchone()
        connection.close()
        print_check("SQLite", "PASS", f"Python built-in {sqlite3.sqlite_version}; no database server needed")
    except sqlite3.Error as error:
        failed = True
        print_check("SQLite", "FAIL", str(error))

    storage = ROOT / "workshop" / ".workshop-data"
    storage_parent = storage if storage.exists() else storage.parent
    try:
        with tempfile.TemporaryFile(dir=storage_parent):
            pass
        writable = True
    except OSError:
        writable = False
    print_check("Local storage", "PASS" if writable else "FAIL", str(storage_parent))
    failed |= not writable

    project_env = ROOT / ".venv"
    if os.name != "nt" and (project_env / "Scripts" / "python.exe").exists():
        print_check("Environment", "WARN", "Repository .venv is Windows-native; WSL/Linux needs a separate uv environment")

    model = os.getenv("WORKSHOP_MODEL", "ollama/qwen3.5:4b")
    embed_provider = os.getenv("WORKSHOP_EMBEDDING_PROVIDER", "ollama")
    model_url = os.getenv("WORKSHOP_MODEL_BASE_URL", "http://localhost:11434")
    embed_url = os.getenv("WORKSHOP_OLLAMA_EMBED_URL", "http://localhost:11434/api/embeddings")
    embed_model = os.getenv("WORKSHOP_EMBEDDING_MODEL", "nomic-embed-text")

    if model.startswith("ollama/") or embed_provider == "ollama":
        ollama_path = shutil.which("ollama")
        print_check(
            "Ollama CLI",
            "PASS" if ollama_path else "WARN",
            ollama_path or "Not on this OS PATH; a reachable Ollama service can still run on the host",
        )

    if args.offline:
        print_check("Model service", "SKIP", "Offline mode; chat and embeddings were not tested")
    elif model.startswith("ollama/") or embed_provider == "ollama":
        try:
            urls = {ollama_tags_url(model_url if model.startswith("ollama/") else embed_url)}
            if embed_provider == "ollama":
                urls.add(ollama_tags_url(embed_url))
            available: set[str] = set()
            for url in sorted(urls):
                with urlopen(url, timeout=3) as response:
                    available.update(installed_model_names(json.load(response)))
                print_check("Ollama service", "PASS", url)
            required = []
            if model.startswith("ollama/"):
                required.append(model.removeprefix("ollama/"))
            if embed_provider == "ollama":
                required.append(embed_model)
            for name in dict.fromkeys(required):
                present = is_model_present(name, available)
                print_check(f"Model {name}", "PASS" if present else "FAIL", "Downloaded" if present else f"Missing; run: ollama pull {name}")
                failed |= not present
        except (ValueError, OSError, HTTPError, URLError, TimeoutError) as error:
            failed = True
            print_check("Ollama service", "FAIL", f"{error}; start Ollama and check the configured URL")
    else:
        print_check("Chat provider", "SKIP", f"{model}; hosted credentials and availability were not tested")
        if embed_provider == "openai":
            has_key = bool(os.getenv("OPENAI_API_KEY"))
            print_check("OpenAI API key", "PASS" if has_key else "FAIL", "Configured" if has_key else "Not set")
            failed |= not has_key

    if args.advanced:
        failed |= check_advanced(offline=args.offline)

    print("\n" + ("NOT READY: resolve FAIL items above." if failed else "READY: checked prerequisites passed."))
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
