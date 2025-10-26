import asyncio
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from .tools import get_nfl_scores, get_nba_scores, get_nba_rosters

print("Starting sport-suggest-mcp server...", file=sys.stderr, flush=True)

server = Server("sport-suggest-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Return available tools."""
    return [
        Tool(
            name="get_nfl_scores",
            description="Get current NFL scores and game info. Only shows live or upcoming games (filters out completed games). Returns detailed stats including QB/RB/WR leaders, score differentials, pace, and broadcast info.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_nba_scores",
            description="Get current NBA scores and game info. Only shows live or upcoming games (filters out completed games). Returns detailed stats including points/rebounds/assists leaders, score differentials, pace, and broadcast info.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_nba_rosters",
            description="Get current rosters for all NBA teams. **CRITICAL: You MUST call this tool before recommending any NBA games based on players or answering questions about which players are on which teams.** Your training data is outdated - players change teams through trades and free agency. This tool provides the only reliable source for current rosters. Returns team names with all players (positions) and jersey numbers.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Call a tool."""
    if name == "get_nfl_scores":
        result = get_nfl_scores()
        return [TextContent(type="text", text=result)]

    elif name == "get_nba_scores":
        result = get_nba_scores()
        return [TextContent(type="text", text=result)]

    elif name == "get_nba_rosters":
        result = get_nba_rosters()
        return [TextContent(type="text", text=result)]

    raise ValueError(f"Unknown tool: {name}")


async def async_main():
    """Async main function"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


def main():
    """Entry point for the CLI"""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
