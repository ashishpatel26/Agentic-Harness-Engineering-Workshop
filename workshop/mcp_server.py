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


@mcp.tool()
def pizzas_needed(people: int, slices_each: int = 3) -> str:
    """Party planner: how many 8-slice pizzas are needed for this many people."""
    if people < 1 or slices_each < 1:
        raise ValueError("people and slices_each must be positive")
    return f"{-(-people * slices_each // 8)} pizzas"


if __name__ == "__main__":
    mcp.run()
