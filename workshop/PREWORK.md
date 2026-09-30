# Participant pre-work (send one week before)

This workshop assumes basic Python, but no prior agent experience. Complete these steps before arrival so the day can focus on the labs.

1. Install OS-level [`uv`](https://docs.astral.sh/uv/), Python 3.12 (or allow `uv` to install it), and Ollama if using the local model path.
2. Clone or download this repository. On Windows, open PowerShell in the repository root and run `powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1`. On macOS, Linux, or WSL, run `uv sync --locked --python 3.12`.
3. If setup did not create it, copy `.env.example` to `.env` (`Copy-Item .env.example .env` in PowerShell or `cp .env.example .env` in a POSIX shell). Keep the default local settings unless your organizer has supplied an approved hosted-provider setup.
4. For the local path, run `ollama pull qwen2.5:7b` and `ollama pull nomic-embed-text` while on a reliable network. Start Ollama.
5. Run `uv run python tools/check_prerequisites.py` to check packages, local storage, the Ollama service, and both model downloads. Then run `uv run python workshop/00-verify/1-verify_setup.py`. Send the organizer the result or a screenshot of the error, with any keys removed.
6. Open `workshop/00-verify/1-verify_setup.ipynb` in JupyterLab or VS Code and select this project's Python environment.

The smoke test checks the CrewAI import, one chat-model response, and one embedding. Both models are required for the Knowledge and Memory labs. If the local model is too slow or unavailable, ask the organizer for the approved fallback before workshop day. Do not paste credentials into notebooks or send company documents unless the organizer has explicitly approved them for the chosen provider.

Do not share the same `.venv` between Windows and WSL. Delete/recreate the environment when switching platforms, or use separate repository copies.
