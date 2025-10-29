"""
Sports score fetching tools for MCP server - NBA only
Simple data provider - let the LLM do the intelligence!
"""

import requests
import json
from datetime import datetime, timedelta


# Global roster cache
ROSTER_CACHE = {
    "nba_display": None,
    "nba_dict": None,
    "nba_injuries": None,
    "last_updated": None,
}


def get_nba_player_rankings() -> str:
    """
    Get top NBA players ranked by ESPN Rating

    Returns:
        Formatted string with top 50 players and their ESPN ratings
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

    leaders = nba_rating_category.get("leaders", [])[:50]  # Top 50

    result = "NBA Player Rankings (ESPN Rating):\n\n"
    result += "Top 50 Players:\n"

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
        injury_dict = {}

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
                injury_dict[team_abbr] = []
                continue

            athletes = roster_data.get("athletes", [])

            if not athletes:
                result += f"**{team_name} ({team_abbr})** - No roster data\n\n"
                roster_dict[team_abbr] = []
                injury_dict[team_abbr] = []
                continue

            result += f"**{team_name} ({team_abbr})**\n"

            players = []
            player_names = []
            injured_players = []

            for athlete in athletes:
                full_name = athlete.get("fullName", "Unknown")
                jersey = athlete.get("jersey", "")
                position = athlete.get("position", {}).get("abbreviation", "")

                # Check injury status
                injuries = athlete.get("injuries", [])
                is_injured = len(injuries) > 0
                injury_status = injuries[0].get("status", "Out") if is_injured else None

                player_names.append(full_name)

                # Track injured players
                if is_injured:
                    injured_players.append({"name": full_name, "status": injury_status})

                player_str = ""
                if jersey:
                    player_str += f"#{jersey} "
                player_str += full_name
                if position:
                    player_str += f" ({position})"
                if is_injured:
                    player_str += f" - {injury_status}"

                players.append(player_str)

            roster_dict[team_abbr] = player_names
            injury_dict[team_abbr] = injured_players

            if players:
                result += f"  Players: {', '.join(players[:12])}"
                if len(players) > 12:
                    result += f" ... and {len(players) - 12} more"
                result += "\n"

            result += "\n"

        ROSTER_CACHE["nba_display"] = result
        ROSTER_CACHE["nba_dict"] = roster_dict
        ROSTER_CACHE["nba_injuries"] = injury_dict
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


# ============================================================================
# INTERNAL HELPER FUNCTIONS (not exposed as tools)
# ============================================================================


def _fetch_games_data_structured():
    """
    Internal helper: Fetch games as structured data (not formatted string)
    Returns list of game dicts
    """
    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return []

    events = data.get("events", [])

    # Filter out completed games
    active_events = [
        event
        for event in events
        if not event["competitions"][0]["status"]["type"]["completed"]
    ]

    games = []

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

        away_record = away_team.get("records", [{}])[0].get("summary", "0-0")
        home_record = home_team.get("records", [{}])[0].get("summary", "0-0")

        status_type = status["type"]["name"]
        period = status.get("period", 0)
        clock = status.get("displayClock", "")

        # Determine status
        if status_type == "STATUS_IN_PROGRESS":
            game_status = f"LIVE - Q{period} {clock}"
        elif status_type == "STATUS_HALFTIME":
            game_status = "HALFTIME"
        else:
            game_status = f"UPCOMING - {status['type']['detail']}"

        # Broadcasts
        broadcasts = competition.get("broadcasts", [])
        broadcast_names = []
        for b in broadcasts:
            if b.get("names"):
                broadcast_names.extend(b["names"])

        venue = competition.get("venue", {})
        venue_name = venue.get("fullName", "N/A")

        game_dict = {
            "game_id": game_id,
            "game_name": game_name,
            "game_date": game_date,
            "status": game_status,
            "away_team": {
                "name": away_team["team"]["displayName"],
                "abbreviation": away_team["team"]["abbreviation"],
                "record": away_record,
                "score": away_score,
            },
            "home_team": {
                "name": home_team["team"]["displayName"],
                "abbreviation": home_team["team"]["abbreviation"],
                "record": home_record,
                "score": home_score,
            },
            "venue": venue_name,
            "broadcast": broadcast_names,
        }

        games.append(game_dict)

    return games


def _fetch_rankings_data_structured():
    """
    Internal helper: Fetch player rankings as structured data
    Returns list of player dicts
    """
    url = "http://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/seasons/2026/types/2/leaders"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return []

    # Find NBA Rating category
    categories = data.get("categories", [])
    nba_rating_category = None

    for category in categories:
        if category.get("name") == "NBARating":
            nba_rating_category = category
            break

    if not nba_rating_category:
        return []

    leaders = nba_rating_category.get("leaders", [])[:50]  # Top 50

    rankings = []

    for idx, leader in enumerate(leaders, 1):
        rating = leader.get("value", 0)
        athlete_ref = leader.get("athlete", {}).get("$ref")

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

            player_dict = {
                "rank": idx,
                "name": full_name,
                "team": team_abbr,
                "espn_rating": round(rating, 1),
            }

            rankings.append(player_dict)

        except requests.exceptions.RequestException:
            continue

    return rankings


def _fetch_matchup_injuries(away_abbr: str, home_abbr: str) -> dict:
    """
    Fetch detailed injury data for a specific matchup using ESPN's injury API

    Args:
        away_abbr: Away team abbreviation (e.g., "LAL")
        home_abbr: Home team abbreviation (e.g., "MIN")

    Returns:
        Dict with injury details for both teams, including return dates and descriptions
    """
    url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/injuries?team={away_abbr}&team={home_abbr}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        return {"injuries": [], "error": "Could not fetch injury data"}

    injuries = data.get("injuries", [])

    # Organize injuries by team
    matchup_injuries = {"away_team": away_abbr, "home_team": home_abbr, "injuries": []}

    for injury in injuries:
        athlete = injury.get("athlete", {})
        team = athlete.get("team", {})
        details = injury.get("details", {})

        injury_info = {
            "player_name": athlete.get("displayName", "Unknown"),
            "team": team.get("abbreviation", "???"),
            "position": athlete.get("position", {}).get("abbreviation", ""),
            "status": injury.get("status", "Unknown"),
            "injury_type": details.get("type", "Unknown"),
            "return_date": details.get("returnDate"),
            "short_description": injury.get("shortComment", ""),
            "long_description": injury.get("longComment", ""),
        }

        matchup_injuries["injuries"].append(injury_info)

    return matchup_injuries


def _fetch_rosters_data_structured():
    """
    Internal helper: Fetch rosters with injury data as structured data
    Returns dict of {team_abbr: [{"name": str, "injured": bool, "injury_status": str}]}
    """
    # Use cached rosters if available
    if (
        ROSTER_CACHE["nba_dict"] is not None
        and ROSTER_CACHE["nba_injuries"] is not None
    ):
        # Combine roster and injury data
        combined_rosters = {}
        for team_abbr, players in ROSTER_CACHE["nba_dict"].items():
            injured_map = {
                inj["name"]: inj["status"]
                for inj in ROSTER_CACHE["nba_injuries"].get(team_abbr, [])
            }

            combined_rosters[team_abbr] = [
                {
                    "name": player,
                    "injured": player in injured_map,
                    "injury_status": injured_map.get(player),
                }
                for player in players
            ]

        return combined_rosters

    # Otherwise fetch fresh
    now = datetime.now()

    url = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        return {}

    teams = data.get("sports", [{}])[0].get("leagues", [{}])[0].get("teams", [])

    if not teams:
        return {}

    roster_dict = {}
    injury_dict = {}

    for team_data in teams:
        team = team_data.get("team", {})
        team_abbr = team.get("abbreviation", "???")
        team_id = team.get("id")

        roster_url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/roster"

        try:
            roster_response = requests.get(roster_url, timeout=5)
            roster_response.raise_for_status()
            roster_data = roster_response.json()
        except requests.exceptions.RequestException:
            roster_dict[team_abbr] = []
            injury_dict[team_abbr] = []
            continue

        athletes = roster_data.get("athletes", [])

        if not athletes:
            roster_dict[team_abbr] = []
            injury_dict[team_abbr] = []
            continue

        player_list = []
        injured_list = []

        for athlete in athletes:
            full_name = athlete.get("fullName", "Unknown")

            # Check injury status
            injuries = athlete.get("injuries", [])
            is_injured = len(injuries) > 0
            injury_status = injuries[0].get("status", "Out") if is_injured else None

            player_list.append(full_name)

            if is_injured:
                injured_list.append({"name": full_name, "status": injury_status})

        roster_dict[team_abbr] = player_list
        injury_dict[team_abbr] = injured_list

    # Cache it
    ROSTER_CACHE["nba_dict"] = roster_dict
    ROSTER_CACHE["nba_injuries"] = injury_dict
    ROSTER_CACHE["last_updated"] = now

    # Combine and return
    combined_rosters = {}
    for team_abbr, players in roster_dict.items():
        injured_map = {
            inj["name"]: inj["status"] for inj in injury_dict.get(team_abbr, [])
        }

        combined_rosters[team_abbr] = [
            {
                "name": player,
                "injured": player in injured_map,
                "injury_status": injured_map.get(player),
            }
            for player in players
        ]

    return combined_rosters


# ============================================================================
# META TOOL - Combines everything
# ============================================================================


def get_nba_recommendation_data() -> str:
    """
    Get comprehensive NBA data for making intelligent game recommendations

    Returns JSON with:
    - All live/upcoming games with full details
    - Current NBA player rankings (top 50 by ESPN Rating)
    - Full team rosters with injury status for each player
    - Matchup-specific injury reports for each game (with return dates and details)

    This rich dataset enables intelligent recommendations based on:
    - Star power (which top-50 players are HEALTHY and playing)
    - Injury impact (avoid games where stars are out)
    - Competitive balance (team records)
    - Broadcast quality (national vs regional)
    - Game timing (live vs upcoming)
    """
    # Fetch all data
    games = _fetch_games_data_structured()
    rankings = _fetch_rankings_data_structured()
    rosters = _fetch_rosters_data_structured()

    # Fetch matchup-specific injury data for each game
    for game in games:
        away_abbr = game["away_team"]["abbreviation"]
        home_abbr = game["home_team"]["abbreviation"]

        matchup_injuries = _fetch_matchup_injuries(away_abbr, home_abbr)
        game["matchup_injuries"] = matchup_injuries

    # Combine into rich JSON
    combined_data = {
        "metadata": {
            "fetched_at": datetime.now().isoformat(),
            "games_count": len(games),
            "top_players_count": len(rankings),
            "teams_count": len(rosters),
        },
        "games": games,
        "player_rankings": rankings,
        "team_rosters": rosters,
    }

    return json.dumps(combined_data, indent=2)
