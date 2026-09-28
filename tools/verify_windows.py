"""Offline verification for the native Windows workshop environment."""

from __future__ import annotations

import asyncio
import os
import platform
import sys
from pathlib import Path

import crewai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]


async def verify_mcp_subprocess() -> tuple[list[str], str]:
    """Start the local stdio MCP server with the current Windows interpreter."""
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(ROOT / "workshop" / "mcp_server.py")],
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            response = await session.list_tools()
            tool_names = [tool.name for tool in response.tools]
            if "annual_roi" not in tool_names:
                raise RuntimeError(f"annual_roi was not discovered: {tool_names}")

            result = await session.call_tool(
                "annual_roi",
                {"annual_benefit": 45_000, "annual_cost": 30_000},
            )
            text = "\n".join(
                item.text for item in result.content if hasattr(item, "text")
            )
            if result.isError or "50.0%" not in text:
                raise RuntimeError(f"Unexpected annual_roi result: {text}")
            return tool_names, text


async def main() -> None:
    if os.name != "nt":
        raise RuntimeError("This verification command must run with native Windows Python.")

    expected_python = ROOT / ".venv" / "Scripts" / "python.exe"
    if Path(sys.executable).resolve() != expected_python.resolve():
        raise RuntimeError(
            f"Expected {expected_python}, but uv selected {sys.executable}."
        )

    tool_names, result = await asyncio.wait_for(verify_mcp_subprocess(), timeout=30)

    print(f"Python: {sys.version.split()[0]} ({platform.system()})")
    print(f"Interpreter: {sys.executable}")
    print(f"CrewAI: {crewai.__version__}")
    print(f"MCP tools: {', '.join(tool_names)}")
    print(f"MCP result: {result}")
    print("Windows verification passed.")


if __name__ == "__main__":
    asyncio.run(main())