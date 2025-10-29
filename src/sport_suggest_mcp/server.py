import asyncio
import sys
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
from .tools import (
    get_nba_scores,
    get_nba_rosters,
    get_nba_player_rankings,
    get_nba_recommendation_data,
)

print("Starting sport-suggest-mcp server...", file=sys.stderr, flush=True)

server = Server("sport-suggest-mcp")


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Return available tools."""
    return [
        Tool(
            name="get_nba_recommendation_data",
            description="""Get comprehensive NBA data for making game recommendations.
    
    Returns JSON containing:
    • games: All live/upcoming games with teams, records, scores, broadcast, venue
      - Each game now includes matchup_injuries with detailed injury reports for both teams
    • player_rankings: Top 25 players ranked by ESPN Rating (higher = better)
    • team_rosters: Complete rosters with injury status for each player
    
    CRITICAL - INJURY CHECK WORKFLOW:
    1. Each game object contains a "matchup_injuries" field with current injury data
    2. Check matchup_injuries to see which players are Out/Questionable for that specific game
    3. Cross-reference with player_rankings to see if any top-25 stars are injured
    4. Only recommend games where the star players are healthy
    
    **DO NOT recommend a game and then correct yourself. Check injuries FIRST.**
    
    Each injury in matchup_injuries includes:
    - player_name: Full name of injured player
    - team: Team abbreviation
    - position: Player position
    - status: "Out", "Questionable", "Day-To-Day", etc.
    - injury_type: Type of injury (e.g., "Knee", "Ankle")
    - return_date: Expected return date (YYYY-MM-DD format)
    - short_description: Brief injury update
    - long_description: Detailed injury context
    
    Example workflow:
    - Game: LAL @ MIN
    - Check matchup_injuries for this game
    - See: Luka Doncic (LAL) - Status: "Out", Return: "2025-11-05"
    - Cross-check: Luka is ranked #1 in player_rankings
    - Result: Lakers missing their top star - consider a different game
    
    Additional factors for recommendations:
    - Competitive balance: Compare team records for close matchups
    - Broadcast quality: National channels (ESPN, TNT, ABC) > regional
    - Game timing: Consider user's time zone preferences
    
    The data is rich enough to support any recommendation style - star power, competitiveness, 
    broadcast quality, or any combination the user requests.""",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_nba_rosters",
            description="""Get current rosters for all NBA teams with injury information (cached, refreshes every 24 hours).
            
            Returns complete player lists with positions, jersey numbers, and injury status for all 30 NBA teams.
            
            Use this when:
            - User asks specifically about team rosters ("Show me the Celtics roster")
            - User asks about a specific player's team ("Is LeBron on the Lakers?")
            - User asks about injuries ("Who's injured on the Lakers?")
            
            For recommendations, use get_nba_recommendation_data() instead - it includes rosters plus everything else!""",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="get_nba_player_rankings",
            description="""Get current NBA player rankings using ESPN's official rating system.
            
            Returns top 25 players with:
            - Player name
            - Team abbreviation
            - ESPN Rating (composite score of offensive/defensive performance)
            
            Use this when:
            - User asks specifically about player rankings ("Who are the best players this season?")
            - User wants to know how a specific player ranks
            
            For recommendations, use get_nba_recommendation_data() instead - it includes rankings plus everything else!""",
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
    if name == "get_nba_recommendation_data":
        result = get_nba_recommendation_data()
        return [TextContent(type="text", text=result)]

    elif name == "get_nba_scores":
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
