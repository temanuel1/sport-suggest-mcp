"""
Sports score fetching tools for MCP server - NBA only
Simple data provider - let the LLM do the intelligence!
"""

import requests
from datetime import datetime, timedelta


# Global roster cache
ROSTER_CACHE = {"nba_display": None, "nba_dict": None, "last_updated": None}


def get_nba_player_rankings() -> str:
    """
    Get top NBA players ranked by ESPN Rating

    Returns:
        Formatted string with top 25 players and their ESPN ratings
    """
    url = "http://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2026/types/2/leaders"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching NBA player rankings: {e}"

    # Find NBA Rating category dynamically
    categories = data.get("categories", [])
    nba_rating_category = None

    for category in categories:
        if category.get("name") == "NBARating":
            nba_rating_category = category
            break

    if not nba_rating_category:
        return "Error: NBA Rating category not found in API response"

    leaders = nba_rating_category.get("leaders", [])[:25]  # Top 25

    result = "NBA Player Rankings (ESPN Rating):\n\n"
    result += "Top 25 Players:\n"

    for idx, leader in enumerate(leaders, 1):
        rating = leader.get("value", 0)
        athlete_ref = leader.get("athlete", {}).get("$ref")

        # Fetch player details
        try:
            player_resp = requests.get(athlete_ref, timeout=5)
            player_resp.raise_for_status()
            player_data = player_resp.json()

            full_name = player_data.get("fullName", "Unknown")
            team_ref = player_data.get("team", {}).get("$ref")

            # Get team abbreviation
            team_abbr = "FA"
            if team_ref:
                try:
                    team_resp = requests.get(team_ref, timeout=3)
                    team_resp.raise_for_status()
                    team_data = team_resp.json()
                    team_abbr = team_data.get("abbreviation", "FA")
                except:
                    pass

            result += f"{idx}. {full_name} ({team_abbr}) - Rating: {rating:.1f}\n"

        except requests.exceptions.RequestException:
            result += f"{idx}. Unknown Player - Rating: {rating:.1f}\n"

    return result


def get_nba_rosters() -> str:
    """
    Get current rosters for all NBA teams (cached, refreshes every 24 hours)

    Returns:
        Formatted string with all NBA team rosters
    """
    now = datetime.now()

    # Check if cache needs refresh
    if (
        ROSTER_CACHE["nba_display"] is None
        or ROSTER_CACHE["last_updated"] is None
        or now - ROSTER_CACHE["last_updated"] > timedelta(hours=24)
    ):

        url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return f"Error fetching NBA teams: {e}"

        teams = data.get("sports", [{}])[0].get("leagues", [{}])[0].get("teams", [])

        if not teams:
            return "No NBA teams found."

        result = "NBA Team Rosters:\n\n"
        roster_dict = {}

        for team_data in teams:
            team = team_data.get("team", {})
            team_name = team.get("displayName", "Unknown Team")
            team_abbr = team.get("abbreviation", "???")
            team_id = team.get("id")

            roster_url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/roster"

            try:
                roster_response = requests.get(roster_url, timeout=5)
                roster_response.raise_for_status()
                roster_data = roster_response.json()
            except requests.exceptions.RequestException:
                result += f"**{team_name} ({team_abbr})** - Roster unavailable\n\n"
                roster_dict[team_abbr] = []
                continue

            athletes = roster_data.get("athletes", [])

            if not athletes:
                result += f"**{team_name} ({team_abbr})** - No roster data\n\n"
                roster_dict[team_abbr] = []
                continue

            result += f"**{team_name} ({team_abbr})**\n"

            players = []
            player_names = []

            for athlete in athletes:
                full_name = athlete.get("fullName", "Unknown")
                jersey = athlete.get("jersey", "")
                position = athlete.get("position", {}).get("abbreviation", "")

                player_names.append(full_name)

                player_str = ""
                if jersey:
                    player_str += f"#{jersey} "
                player_str += full_name
                if position:
                    player_str += f" ({position})"

                players.append(player_str)

            roster_dict[team_abbr] = player_names

            if players:
                result += f"  Players: {', '.join(players[:12])}"
                if len(players) > 12:
                    result += f" ... and {len(players) - 12} more"
                result += "\n"

            result += "\n"

        ROSTER_CACHE["nba_display"] = result
        ROSTER_CACHE["nba_dict"] = roster_dict
        ROSTER_CACHE["last_updated"] = now

        return result

    return ROSTER_CACHE["nba_display"]


def get_nba_scores() -> str:
    """
    Get current NBA scores and upcoming games - RAW DATA ONLY

    Returns:
        Formatted string with game information (no calculated metrics)
    """
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching NBA scores: {e}"

    events = data.get("events", [])

    # Filter out completed games
    active_events = [
        event
        for event in events
        if not event["competitions"][0]["status"]["type"]["completed"]
    ]

    if not active_events:
        return "No live or upcoming NBA games found for today."

    result = f"Found {len(active_events)} live/upcoming NBA game(s):\n\n"

    for event in active_events:
        competition = event["competitions"][0]
        status = competition["status"]

        home_team = next(
            c for c in competition["competitors"] if c["homeAway"] == "home"
        )
        away_team = next(
            c for c in competition["competitors"] if c["homeAway"] == "away"
        )

        game_id = event["id"]
        game_name = event["shortName"]
        game_date = event["date"]

        away_score = int(away_team.get("score", 0))
        home_score = int(home_team.get("score", 0))
        score_diff = abs(away_score - home_score)

        away_record = away_team.get("records", [{}])[0].get("summary", "0-0")
        home_record = home_team.get("records", [{}])[0].get("summary", "0-0")

        status_type = status["type"]["name"]
        period = status.get("period", 0)
        clock = status.get("displayClock", "")

        if status_type == "STATUS_IN_PROGRESS":
            status_text = f"🔴 LIVE - Q{period} {clock}"
        elif status_type == "STATUS_HALFTIME":
            status_text = f"⏸️  HALFTIME"
        else:
            status_text = f"⏰ UPCOMING - {status['type']['detail']}"

        # Broadcasts
        broadcasts = competition.get("broadcasts", [])
        broadcast_names = []
        for b in broadcasts:
            if b.get("names"):
                broadcast_names.extend(b["names"])

        venue = competition.get("venue", {})
        venue_name = venue.get("fullName", "N/A")

        # Build simple output - NO METRICS
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**{game_name}** (ID: {game_id})\n"
        result += f"📅 {game_date}\n"
        result += f"**Status:** {status_text}\n\n"

        result += f"**Away:** {away_team['team']['displayName']} ({away_record})"
        if away_score > 0:
            result += f" - {away_score}"
        result += "\n"

        result += f"**Home:** {home_team['team']['displayName']} ({home_record})"
        if home_score > 0:
            result += f" - {home_score}"
        result += "\n"

        if away_score > 0 or home_score > 0:
            if away_score > home_score:
                result += f"**Current Leader:** {away_team['team']['abbreviation']} by {score_diff}\n"
            elif home_score > away_score:
                result += f"**Current Leader:** {home_team['team']['abbreviation']} by {score_diff}\n"
            else:
                result += f"**Score:** Tied\n"

        result += f"\n**Venue:** {venue_name}\n"

        if broadcast_names:
            result += f"**Broadcast:** {', '.join(broadcast_names)}\n"

        result += "\n"

    return result
