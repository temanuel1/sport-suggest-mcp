"""
Sports score fetching tools for MCP server
"""

import requests
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_nfl_scores() -> str:
    """
    Get current NFL scores and game info (only live/upcoming games)

    Returns:
        Formatted string with detailed NFL game information
    """
    url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching NFL scores: {e}"

    events = data.get("events", [])

    # Filter out completed games
    active_events = [
        event
        for event in events
        if not event["competitions"][0]["status"]["type"]["completed"]
    ]

    if not active_events:
        return "No live or upcoming NFL games found for today."

    result = f"Found {len(active_events)} live/upcoming NFL game(s):\n\n"

    for event in active_events:
        competition = event["competitions"][0]
        status = competition["status"]

        # Get teams
        home_team = next(
            c for c in competition["competitors"] if c["homeAway"] == "home"
        )
        away_team = next(
            c for c in competition["competitors"] if c["homeAway"] == "away"
        )

        # Basic info
        game_id = event["id"]
        game_name = event["shortName"]
        game_date = event["date"]

        # Scores
        away_score = int(away_team.get("score", 0))
        home_score = int(home_team.get("score", 0))
        score_diff = abs(away_score - home_score)

        # Score leader (renamed to avoid variable collision)
        if away_score > home_score:
            leading_team = (
                f"{away_team['team']['abbreviation']} leading by {score_diff}"
            )
        elif home_score > away_score:
            leading_team = (
                f"{home_team['team']['abbreviation']} leading by {score_diff}"
            )
        else:
            leading_team = "Tied"

        # Quarter scores
        away_quarters = away_team.get("linescores", [])
        home_quarters = home_team.get("linescores", [])

        # Status
        status_type = status["type"]["name"]
        period = status.get("period", 0)
        clock = status.get("displayClock", "")

        if status_type == "STATUS_IN_PROGRESS":
            quarter_names = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}
            status_text = f"LIVE - {quarter_names.get(period, f'Q{period}')} {clock}"
        elif status_type == "STATUS_HALFTIME":
            status_text = f"HALFTIME"
        else:
            status_text = f"UPCOMING - {status['type']['detail']}"

        # Records
        away_record = away_team.get("records", [{}])[0].get("summary", "N/A")
        home_record = home_team.get("records", [{}])[0].get("summary", "N/A")

        # NFL-specific leaders (at competition level)
        away_leaders = {}
        home_leaders = {}

        competition_leaders = competition.get("leaders", [])
        leader_types = ["passingYards", "rushingYards", "receivingYards"]

        for leader_type in leader_types:
            leader_category = next(
                (l for l in competition_leaders if l.get("name") == leader_type),
                None,
            )

            if leader_category and leader_category.get("leaders"):
                # Fixed: renamed 'leader' to 'player_leader' to avoid variable collision
                for player_leader in leader_category["leaders"]:
                    leader_team_id = player_leader.get("team", {}).get("id")

                    if leader_team_id == home_team["team"]["id"]:
                        home_leaders[leader_type] = {
                            "name": player_leader["athlete"]["fullName"],
                            "value": player_leader["displayValue"],
                        }
                    elif leader_team_id == away_team["team"]["id"]:
                        away_leaders[leader_type] = {
                            "name": player_leader["athlete"]["fullName"],
                            "value": player_leader["displayValue"],
                        }

        # Context
        venue = competition.get("venue", {})
        venue_name = venue.get("fullName", "N/A")
        attendance = competition.get("attendance", 0)
        conference_game = competition.get("conferenceCompetition", False)

        # Broadcasts
        broadcasts = competition.get("broadcasts", [])
        broadcast_names = []
        for b in broadcasts:
            if b.get("names"):
                broadcast_names.extend(b["names"])

        # Notes
        notes = competition.get("notes", [])
        notes_text = [n.get("headline", "") for n in notes if n.get("headline")]

        # Calculated metrics
        total_points = away_score + home_score
        pace = "N/A"
        if status_type == "STATUS_IN_PROGRESS" and period > 0:
            pace = f"{total_points / period:.1f} pts/period"

        # Build output
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**{game_name}** (ID: {game_id})\n"
        result += f"{game_date}\n\n"

        result += f"**Away:** {away_team['team']['displayName']} ({away_record}) - {away_score}\n"
        if away_quarters:
            result += f"  Quarters: {', '.join([str(int(q.get('value', 0))) for q in away_quarters])}\n"

        result += f"**Home:** {home_team['team']['displayName']} ({home_record}) - {home_score}\n"
        if home_quarters:
            result += f"  Quarters: {', '.join([str(int(q.get('value', 0))) for q in home_quarters])}\n"

        result += f"\n**Status:** {status_text}\n"

        # Score context for live games
        if status_type == "STATUS_IN_PROGRESS":
            result += f"**Score Differential:** {score_diff} points ({leading_team})\n"
            result += f"**Total Points:** {total_points}\n"
            result += f"**Pace:** {pace}\n"

        # NFL-specific leader display - ONLY FOR LIVE GAMES
        if (away_leaders or home_leaders) and status_type == "STATUS_IN_PROGRESS":
            result += f"\n**Top Performers:**\n"

            if away_leaders.get("passingYards"):
                result += f"  Away QB: {away_leaders['passingYards']['name']} - {away_leaders['passingYards']['value']}\n"
            if home_leaders.get("passingYards"):
                result += f"  Home QB: {home_leaders['passingYards']['name']} - {home_leaders['passingYards']['value']}\n"

            if away_leaders.get("rushingYards"):
                result += f"  Away RB: {away_leaders['rushingYards']['name']} - {away_leaders['rushingYards']['value']}\n"
            if home_leaders.get("rushingYards"):
                result += f"  Home RB: {home_leaders['rushingYards']['name']} - {home_leaders['rushingYards']['value']}\n"

            if away_leaders.get("receivingYards"):
                result += f"  Away WR: {away_leaders['receivingYards']['name']} - {away_leaders['receivingYards']['value']}\n"
            if home_leaders.get("receivingYards"):
                result += f"  Home WR: {home_leaders['receivingYards']['name']} - {home_leaders['receivingYards']['value']}\n"

        result += f"\n**Venue:** {venue_name}\n"
        if attendance > 0:
            result += f"**Attendance:** {attendance:,}\n"
        if conference_game:
            result += f"**Conference Game:** Yes\n"
        if broadcast_names:
            result += f"**Watch:** {', '.join(broadcast_names)}\n"
        if notes_text:
            result += f"**Notes:** {'; '.join(notes_text)}\n"

        result += "\n"

    return result


def get_nba_scores() -> str:
    """
    Get current NBA scores and game info (only live/upcoming games)

    Returns:
        Formatted string with detailed NBA game information
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

        # Get teams
        home_team = next(
            c for c in competition["competitors"] if c["homeAway"] == "home"
        )
        away_team = next(
            c for c in competition["competitors"] if c["homeAway"] == "away"
        )

        # Basic info
        game_id = event["id"]
        game_name = event["shortName"]
        game_date = event["date"]

        # Scores
        away_score = int(away_team.get("score", 0))
        home_score = int(home_team.get("score", 0))
        score_diff = abs(away_score - home_score)

        # Score leader (renamed to avoid variable collision)
        if away_score > home_score:
            leading_team = (
                f"{away_team['team']['abbreviation']} leading by {score_diff}"
            )
        elif home_score > away_score:
            leading_team = (
                f"{home_team['team']['abbreviation']} leading by {score_diff}"
            )
        else:
            leading_team = "Tied"

        # Quarter scores
        away_quarters = away_team.get("linescores", [])
        home_quarters = home_team.get("linescores", [])

        # Status
        status_type = status["type"]["name"]
        period = status.get("period", 0)
        clock = status.get("displayClock", "")

        if status_type == "STATUS_IN_PROGRESS":
            status_text = f"LIVE - Q{period} {clock}"
        elif status_type == "STATUS_HALFTIME":
            status_text = f"HALFTIME"
        else:
            status_text = f"UPCOMING - {status['type']['detail']}"

        # Records
        away_record = away_team.get("records", [{}])[0].get("summary", "N/A")
        home_record = home_team.get("records", [{}])[0].get("summary", "N/A")

        # NBA-specific leaders (at team/competitor level)
        away_leaders = {}
        home_leaders = {}

        leader_types = ["points", "rebounds", "assists"]

        for leader_type in leader_types:
            # Away team leaders
            away_leader_data = next(
                (
                    l
                    for l in away_team.get("leaders", [])
                    if l.get("name") == leader_type
                ),
                None,
            )
            if away_leader_data and away_leader_data.get("leaders"):
                top = away_leader_data["leaders"][0]
                away_leaders[leader_type] = {
                    "name": top["athlete"]["fullName"],
                    "value": top["displayValue"],
                }

            # Home team leaders
            home_leader_data = next(
                (
                    l
                    for l in home_team.get("leaders", [])
                    if l.get("name") == leader_type
                ),
                None,
            )
            if home_leader_data and home_leader_data.get("leaders"):
                top = home_leader_data["leaders"][0]
                home_leaders[leader_type] = {
                    "name": top["athlete"]["fullName"],
                    "value": top["displayValue"],
                }

        # Context
        venue = competition.get("venue", {})
        venue_name = venue.get("fullName", "N/A")
        attendance = competition.get("attendance", 0)
        conference_game = competition.get("conferenceCompetition", False)

        # Broadcasts
        broadcasts = competition.get("broadcasts", [])
        broadcast_names = []
        for b in broadcasts:
            if b.get("names"):
                broadcast_names.extend(b["names"])

        # Notes
        notes = competition.get("notes", [])
        notes_text = [n.get("headline", "") for n in notes if n.get("headline")]

        # Calculated metrics
        total_points = away_score + home_score
        pace = "N/A"
        if status_type == "STATUS_IN_PROGRESS" and period > 0:
            pace = f"{total_points / period:.1f} pts/quarter"

        # Build output
        result += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        result += f"**{game_name}** (ID: {game_id})\n"
        result += f"{game_date}\n\n"

        result += f"**Away:** {away_team['team']['displayName']} ({away_record}) - {away_score}\n"
        if away_quarters:
            result += f"  Quarters: {', '.join([str(int(q.get('value', 0))) for q in away_quarters])}\n"

        result += f"**Home:** {home_team['team']['displayName']} ({home_record}) - {home_score}\n"
        if home_quarters:
            result += f"  Quarters: {', '.join([str(int(q.get('value', 0))) for q in home_quarters])}\n"

        result += f"\n**Status:** {status_text}\n"

        # Score context for live games
        if status_type == "STATUS_IN_PROGRESS":
            result += f"**Score Differential:** {score_diff} points ({leading_team})\n"
            result += f"**Total Points:** {total_points}\n"
            result += f"**Pace:** {pace}\n"

        # NBA-specific leader display - ONLY FOR LIVE GAMES
        if (away_leaders or home_leaders) and status_type == "STATUS_IN_PROGRESS":
            result += f"\n**Top Performers:**\n"

            if away_leaders.get("points"):
                result += f"  Away: {away_leaders['points']['name']} - {away_leaders['points']['value']} PTS"
                if away_leaders.get("rebounds"):
                    result += f", {away_leaders['rebounds']['value']} REB"
                if away_leaders.get("assists"):
                    result += f", {away_leaders['assists']['value']} AST"
                result += "\n"

            if home_leaders.get("points"):
                result += f"  Home: {home_leaders['points']['name']} - {home_leaders['points']['value']} PTS"
                if home_leaders.get("rebounds"):
                    result += f", {home_leaders['rebounds']['value']} REB"
                if home_leaders.get("assists"):
                    result += f", {home_leaders['assists']['value']} AST"
                result += "\n"

        result += f"\n**Venue:** {venue_name}\n"
        if attendance > 0:
            result += f"**Attendance:** {attendance:,}\n"
        if conference_game:
            result += f"**Conference Game:** Yes\n"
        if broadcast_names:
            result += f"**Watch:** {', '.join(broadcast_names)}\n"
        if notes_text:
            result += f"**Notes:** {'; '.join(notes_text)}\n"

        result += "\n"

    return result


def get_nba_rosters() -> str:
    """
    Get current rosters for all NBA teams

    Returns:
        Formatted string with all NBA team rosters
    """
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

    for team_data in teams:
        team = team_data.get("team", {})
        team_name = team.get("displayName", "Unknown Team")
        team_abbr = team.get("abbreviation", "???")

        # Fetch roster for this team
        team_id = team.get("id")
        roster_url = f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/roster"

        try:
            roster_response = requests.get(roster_url, timeout=5)
            roster_response.raise_for_status()
            roster_data = roster_response.json()
        except requests.exceptions.RequestException:
            result += f"**{team_name} ({team_abbr})** - Roster unavailable\n\n"
            continue

        # Parse roster - athletes is a FLAT array, not grouped
        athletes = roster_data.get("athletes", [])

        if not athletes:
            result += f"**{team_name} ({team_abbr})** - No roster data\n\n"
            continue

        result += f"**{team_name} ({team_abbr})**\n"

        # Get all players from the flat array
        players = []
        for athlete in athletes:
            full_name = athlete.get("fullName", "Unknown")
            jersey = athlete.get("jersey", "")
            position = athlete.get("position", {}).get("abbreviation", "")

            # Format: #24 Kobe Bryant (G)
            player_str = ""
            if jersey:
                player_str += f"#{jersey} "
            player_str += full_name
            if position:
                player_str += f" ({position})"

            players.append(player_str)

        if players:
            result += "  Players:\n"
            for p in players:
                result += f"    {p}\n"
        result += "\n"

    return result
