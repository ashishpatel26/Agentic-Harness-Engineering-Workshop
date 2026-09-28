"""Local, read-only MCP server used by the CrewAI MCP lesson."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from mcp.server.fastmcp import FastMCP

from workshop.tools import calculate_annual_roi

mcp = FastMCP("Northstar Research Tools")


@mcp.tool()
def annual_roi(annual_benefit: float, annual_cost: float) -> str:
    """Calculate hypothetical annual ROI percentage from USD assumptions."""
    return f"Scenario ROI: {calculate_annual_roi(annual_benefit, annual_cost)}%"


if __name__ == "__main__":
    mcp.run()
