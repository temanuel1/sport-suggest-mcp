import asyncio
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from .tools import get_nba_scores, get_nba_rosters, get_nba_player_rankings

print("Starting sport-suggest-mcp server...", file=sys.stderr, flush=True)

server = Server("sport-suggest-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Return available tools."""
    return [
        Tool(
            name="get_nba_scores",
            description="""Get current NBA scores and upcoming games with basic information.
            
            Returns for each game:
            - Team names and records (e.g., "Lakers (5-2)")
            - Current score (for live games)
            - Game status (upcoming time, live quarter/clock, halftime)
            - Broadcast channels
            - Venue
            
            This tool provides RAW DATA only. Use your intelligence to:
            - Cross-reference with get_nba_player_rankings() to identify star matchups
            - Compare team records to assess competitiveness
            - Evaluate broadcast quality (national vs regional)
            - Consider game timing for user convenience
            - Make personalized recommendations based on user preferences
            
            When recommending games, call get_nba_player_rankings() first to know which players are elite, then use get_nba_rosters() to see which stars are playing in each game.""",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_nba_rosters",
            description="""Get current rosters for all NBA teams (cached, refreshes every 24 hours).
            
            Returns complete player lists with positions and jersey numbers for all 30 NBA teams.
            
            Use this when:
            - User asks about specific players ("Is LeBron on the Lakers?", "Show me the Celtics roster")
            - You need to check which elite players (from get_nba_player_rankings) are on teams playing today
            - User wants to see team rosters independently of game information
            
            To identify star matchups:
            1. Call get_nba_player_rankings() to see top 50 players
            2. Call get_nba_scores() to see today's games
            3. Call get_nba_rosters() to cross-reference which stars are on which teams
            4. Make intelligent recommendation""",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_nba_player_rankings",
            description="""Get current NBA player rankings using ESPN's official rating system.
            
            Returns top 50 players with:
            - Player name
            - Team abbreviation
            - ESPN Rating (composite score of offensive/defensive performance)
            
            This represents ESPN's authoritative ranking of the best players RIGHT NOW based on current season performance.
            
            Use this to:
            - Identify which players are elite/stars this season
            - Find games with top talent when user asks for "star power"
            - Cross-reference with rosters to see which stars are playing tonight
            - Provide context on player quality when discussing games
            
            Typical workflow for game recommendations:
            1. Call this tool to see who the best players are
            2. Call get_nba_scores() to see today's games  
            3. Call get_nba_rosters() to match stars to teams
            4. Recommend games with the most top-50 players""",
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
    if name == "get_nba_scores":
        result = get_nba_scores()
        return [TextContent(type="text", text=result)]

    elif name == "get_nba_rosters":
        result = get_nba_rosters()
        return [TextContent(type="text", text=result)]

    elif name == "get_nba_player_rankings":
        result = get_nba_player_rankings()
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
