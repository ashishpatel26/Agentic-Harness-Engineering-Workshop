FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.11.23 /uv /uvx /usr/local/bin/
WORKDIR /app
ENV UV_NO_DEV=1 UV_COMPILE_BYTECODE=1 PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --extra advanced --no-install-project
COPY workshop ./workshop
COPY tools ./tools
EXPOSE 8000
CMD ["uvicorn", "workshop.api:api", "--host", "0.0.0.0", "--port", "8000"]
