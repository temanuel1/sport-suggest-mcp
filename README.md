# Sport Suggest MCP

Your conversational AI sports companion that tells you what to watch right now.

> **🎯 The Problem:** You want to watch sports, but you don't know what's on or what's worth watching. Existing apps just show you schedules and scores - they don't understand what YOU want to watch right now.
>
> **💡 The Solution:** Sport Suggest MCP turns Claude into your personal sports advisor. Have a conversation about what you're in the mood for, and get instant recommendations for the best games to watch - live right now or coming up soon.

## 🔥 What Makes This Different

**Traditional Sports Apps:**

- Show you everything that's on
- You have to manually browse through scores
- No understanding of what makes a game exciting
- Can't personalize to your mood or preferences

**Sport Suggest MCP + Claude:**

- "Show me something exciting right now" → Claude analyzes score differentials and time remaining to find nail-biters
- "I want a high-scoring game" → Claude looks at pace and total points to suggest offensive shootouts
- "Find me a competitive game" → Claude combines score, time remaining, and team quality to recommend
- "What should I watch tonight?" → Claude reviews upcoming matchups and suggests the best ones
- "Which game has the best players?" → Claude checks **current rosters** to find star-studded matchups

### Real Conversational Examples

**Right Now Recommendations:**

```
You: "What's the most exciting NFL game on right now?"

Claude: The Bengals-Jets game is your best bet - it's 38-32 with
4:36 left in the 4th quarter. That's a 6-point game with enough
time for a comeback, and the pace is insane at 17.5 points per
quarter. Plus it's on CBS.
```

**Star Player Discovery:**

```
You: "Which NBA game should I watch if I want to see some star players?"

Claude: [Checks current rosters] The Bucks @ Cavaliers game has the
most star power right now. Giannis Antetokounmpo (2x MVP) is going
up against Donovan Mitchell and the Cavaliers. Both teams are
playing well and it's a close game at halftime (65-56).
```

**Style-Based Discovery:**

```
You: "I want a defensive battle"

Claude: The Bucs-Saints game is perfect for you. It's 7-3 in the
3rd quarter with a pace of only 3.3 points per period. Both teams
are struggling to move the ball, and the Superdome crowd is into it.
```

**Player Performance Focus:**

```
You: "Any star performances happening right now?"

Claude: Yes! LaMelo Ball is putting on a show with 23 points already
and it's only the 2nd quarter. The Hornets are down 60-51 to the
Wizards but Ball is keeping them in it with his scoring and playmaking.
```

## 🚀 Why This Doesn't Exist Yet

**AI chatbots (ChatGPT, Claude, Gemini) cannot access live sports data.** They're completely blind to:

- What games are on right now
- Current scores and game situations
- Real-time player performances
- Game pace and momentum
- Which players are on which teams (due to trades and roster moves)

Apps like ESPN, Roku, and Samsung TV show you data, but they don't have conversations with you or understand your preferences in the moment.

**Sport Suggest MCP bridges this gap** - combining Claude's conversational intelligence with ESPN's live data to create a personalized sports discovery experience.

## 🛠️ How It Works

Sport Suggest MCP provides Claude with three powerful tools that return rich, structured data. Claude then analyzes this data conversationally to understand what YOU want to watch.

### 1. `get_nfl_scores` - Live & Upcoming NFL Games

Returns all live and upcoming NFL games with comprehensive context.

**Rich data includes:**

- **Score & Momentum:** Current score, score differential, which team is leading
- **Game State:** Quarter, time remaining, whether it's live or upcoming
- **Player Performance:** Top QB (passing yards, TDs), top RB (rushing yards, TDs), top WR (receiving yards, TDs)
- **Context:** Team records, venue, attendance, conference game flag
- **Pace Metrics:** Points per period to identify offensive shootouts vs defensive battles
- **Quarter-by-Quarter Scoring:** See how each team scored across all quarters
- **Broadcast Info:** What channel to watch on

**What Claude can answer with this:**

- "What's the closest game?" → Analyzes score differential + time remaining
- "Show me a shootout" → Looks at pace (points per period) and total points
- "Any star performances?" → Reviews top QB/RB/WR stats
- "Find me a good team matchup" → Compares team records
- "Where can I watch?" → Returns broadcast channel

---

### 2. `get_nba_scores` - Live & Upcoming NBA Games

Returns all live and upcoming NBA games with comprehensive context.

**Rich data includes:**

- **Score & Momentum:** Current score, score differential, which team is leading
- **Game State:** Quarter, time remaining, whether it's live or upcoming
- **Player Performance:** Top scorer with full points/rebounds/assists stat line
- **Context:** Team records, venue, attendance, conference game flag
- **Pace Metrics:** Points per quarter to identify fast-paced vs slow-paced games
- **Quarter-by-Quarter Scoring:** Track scoring trends across all quarters
- **Broadcast Info:** What channel to watch on

**What Claude can answer with this:**

- "Find me a close game" → Filters by score differential in late quarters
- "Any triple-doubles happening?" → Reviews stat lines
- "Show me a high-scoring game" → Analyzes pace and total points
- "What's the best rivalry game?" → Combines team quality with competitiveness
- "Where can I watch Lakers games?" → Returns broadcast info

---

### 3. `get_nba_rosters` - Current NBA Team Rosters ✨ NEW

Returns up-to-date rosters for all NBA teams with complete player information.

**Rich data includes:**

- **Complete rosters:** All players for every NBA team
- **Player details:** Jersey numbers and positions
- **Always current:** Reflects latest trades, signings, and roster moves

**Why this matters:**

NBA rosters change constantly through trades, free agency, and signings. Claude's training data becomes outdated quickly. This tool ensures Claude always has the most current information about which players are on which teams.

**What Claude can answer with this:**

- "Which game has the best players?" → Checks current rosters to find star matchups
- "Is LeBron playing tonight?" → Verifies current team roster
- "Show me a game with good young talent" → Identifies rising stars on current rosters
- "Which teams have the most All-Stars?" → Analyzes roster quality

**How it works:**

When you ask about players or star power, Claude automatically checks current rosters before making recommendations. This ensures accuracy even when major roster moves have happened since Claude's training data cutoff.

## 🎯 The Personalization Magic

The key insight: **We don't hardcode recommendations.** Instead, we give Claude rich data and let it reason conversationally about what YOU want.

### How Personalization Emerges Naturally:

**User says:** "I want something exciting"  
**Claude reasons:** _Score differential < 10 AND 4th quarter AND time remaining < 5 minutes = exciting_

**User says:** "Find me a blowout to have on in the background"  
**Claude reasons:** _Score differential > 20 AND early game = background viewing_

**User says:** "Show me a game with a star player going off"  
**Claude reasons:** _Top scorer has 40+ points OR QB has 300+ yards and 3 TDs = star performance_

**User says:** "I want to watch good teams"  
**Claude reasons:** _Both teams have winning records (>0.500) = quality matchup_

**User says:** "Which game has the most star power?"  
**Claude reasons:** _[Checks rosters] → Identifies games with multiple All-Stars and MVP-caliber players_

This approach is infinitely flexible - as your preferences evolve in the conversation, Claude adapts without any code changes.

## 🏗️ Project Structure

```
sport-suggest-mcp/
├── src/
│   └── sport_suggest_mcp/
│       ├── __init__.py
│       ├── server.py           # MCP server setup & tool registration
│       └── tools.py            # get_nfl_scores, get_nba_scores, get_nba_rosters
├── pyproject.toml              # Python project configuration
└── README.md
```

## 📡 ESPN API Endpoints

This project uses ESPN's unofficial public API (no API key required):

**NFL Scoreboard:**

```
https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard
```

**NBA Scoreboard:**

```
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard
```

**NBA Team Rosters:**

```
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams
https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/{team_id}/roster
```

**Data returned includes:**

- Live scores and game status (quarter, time remaining)
- Team information (names, records, abbreviations)
- Statistical leaders (top performers for each team)
- Venue and broadcast details
- Quarter-by-quarter scoring breakdowns
- Complete team rosters with player positions and jersey numbers

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Claude Desktop
- uv (Python package installer)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sport-suggest-mcp.git
cd sport-suggest-mcp

# Install with uv
uv pip install -e .
```

### Configuration

Add to your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sport-suggest": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/sport-suggest-mcp",
        "run",
        "sport-suggest-mcp"
      ]
    }
  }
}
```

**Important:** Replace `/ABSOLUTE/PATH/TO/sport-suggest-mcp` with the actual absolute path to your project directory.

Restart Claude Desktop, and you're ready to start discovering games!

## 💬 Example Queries to Try

### Finding Games Right Now

- "What NFL games are on right now?"
- "Show me the most exciting NBA game"
- "Find me a close football game"
- "What's the highest scoring game on?"
- "Any nail-biters happening?"

### Style Preferences

- "I want a defensive battle"
- "Show me an offensive shootout"
- "Find me a high-paced game"
- "I want to watch a competitive game"

### Player-Focused ✨ Enhanced with Roster Data

- "Any star performances happening?"
- "Which game has the best players?" ← Uses current rosters
- "Show me games with great QB play"
- "Which NBA game should I watch for star power?" ← Uses current rosters
- "Are there any players going off right now?"
- "Is Giannis playing tonight?" ← Checks current roster

### Team-Based

- "Should I watch the Cowboys game?"
- "Show me games with winning teams"
- "Find me a good matchup"
- "Any rivalry games on?"

### Upcoming Games

- "What NFL games are coming up tonight?"
- "What should I watch this weekend?"
- "When does the Lakers game start?"
- "Which upcoming game has the most star power?" ← Uses current rosters

## 🗺️ Development Roadmap

### ✅ Phase 1: Core Discovery (Complete)

- [x] MCP server setup with Python
- [x] ESPN API client with NFL & NBA support
- [x] `get_nfl_scores` with rich player/game data
- [x] `get_nba_scores` with rich player/game data
- [x] `get_nba_rosters` with current roster information
- [x] Filtering out completed games
- [x] Real-time player performance tracking
- [x] Automatic roster checking for star player recommendations

### 🚧 Phase 2: Enhanced Intelligence (In Progress)

- [ ] Add `get_nfl_rosters` for current NFL rosters
- [ ] Add playoff implications detection
- [ ] Team momentum indicators (recent win/loss streaks)
- [ ] Injury impact analysis
- [ ] Historical rivalry context

### 📅 Phase 3: Expanded Coverage

- [ ] Add NHL support
- [ ] Add MLB support
- [ ] Add college sports (NCAAF, NCAAB)
- [ ] International soccer leagues

### 🔮 Phase 4: Advanced Features

- [ ] `get_game_details(game_id)` for deep-dive analysis
- [ ] Play-by-play highlights for live games
- [ ] Betting line integration
- [ ] "Games like this" historical comparisons

## 🎓 Key Design Philosophy

### Let Claude Be the Conversation Expert

We don't build rigid recommendation algorithms. Instead:

1. **We provide rich data** - scores, player stats, pace metrics, team records, **current rosters**
2. **Claude analyzes conversationally** - "This game is close AND has a high pace AND features star performers"
3. **Recommendations feel natural** - like talking to a knowledgeable friend, not querying a database

### Always Use Fresh Data

Sports rosters change constantly. Rather than relying on Claude's training data:

- **Automatic roster checking** - Claude queries current rosters when discussing players
- **Trade-proof recommendations** - Always accurate even after major roster moves
- **No manual updates needed** - Roster data is fetched live from ESPN's API

### Data-Driven But Not Prescriptive

Every game includes enough context for Claude to make intelligent recommendations:

- **Stakes:** Team records, conference games
- **Style:** Pace metrics, scoring patterns, defensive vs offensive battles
- **Talent:** Player performance leaders (QB/RB/WR for NFL, PTS/REB/AST for NBA)
- **Roster Quality:** Current team rosters with star players identified
- **Timing:** Quarter/time remaining, halftime, upcoming
- **Accessibility:** Broadcast channel, venue, attendance

This lets Claude understand not just WHAT is happening, but WHY it matters to YOU.

### Personalization Through Conversation

Instead of profile settings, preferences emerge naturally through dialogue:

- "I love defense" → Claude prioritizes low-pace, close games
- "I'm a casual fan" → Claude explains context and storylines
- "I only have 20 minutes" → Claude finds games in the 4th quarter
- "Show me star power" → Claude checks rosters and highlights top-tier matchups

## 📊 Success Metrics

- ✅ Recommend a relevant game in <2 seconds
- ✅ Understand conversational preferences ("exciting", "close", "high-scoring", "star power")
- ✅ Handle NFL and NBA reliably with live data
- ✅ Always use current rosters for player-based recommendations
- ✅ Gracefully explain when nothing interesting is on
- ✅ Feel like talking to a knowledgeable sports friend

## 🔧 Technical Details

### Why Python?

- Simple, readable code for sports data parsing
- Excellent support for REST APIs via `requests`
- Fast development iteration
- Easy integration with MCP Python SDK

### Why Three Separate Tools?

We use `get_nfl_scores()`, `get_nba_scores()`, and `get_nba_rosters()` as separate tools because:

1. **Simpler for Claude** - Direct function calls vs parameter passing
2. **Sport-specific logic** - NFL uses QB/RB/WR leaders, NBA uses PTS/REB/AST, rosters are NBA-specific
3. **Performance** - Only fetch rosters when needed for player-based queries
4. **Easier to extend** - Add `get_nfl_rosters()` or `get_mlb_scores()` later without touching existing code

### Data Parsing Strategy

NFL and NBA have different API structures:

**NFL:** Leaders at the competition level (shared across both teams)

```python
competition.get("leaders", [])  # Contains all players from both teams
```

**NBA:** Leaders at the team/competitor level (separated by team)

```python
away_team.get("leaders", [])  # Away team players
home_team.get("leaders", [])  # Home team players
```

**NBA Rosters:** Flat array structure

```python
roster_data.get("athletes", [])  # All players in single array
```

Our tool functions handle these differences internally, presenting clean, consistent data to Claude.

### Ensuring Fresh Roster Data

The `get_nba_rosters` tool description includes explicit instructions to Claude:

> **CRITICAL: You MUST call this tool before recommending any NBA games based on players or answering questions about which players are on which teams.** Your training data is outdated - players change teams through trades and free agency. This tool provides the only reliable source for current rosters.

This ensures Claude always checks rosters rather than relying on potentially outdated training data.

## 🐛 Known Issues & Limitations

- **Attendance data is unreliable** - ESPN doesn't always populate it, even for live games
- **Halftime detection** - Some edge cases during halftime transitions
- **Season stats vs game stats** - For upcoming games, API sometimes returns season totals instead of game stats (we filter these out)
- **NFL rosters not yet implemented** - Currently only NBA has roster checking

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [ESPN API Unofficial Docs](https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b)

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! This is a learning project exploring the intersection of AI and sports discovery.

**Ideas we'd love help with:**

- NFL roster tool implementation
- Additional sports (MLB, NHL, soccer)
- Better playoff implications detection using standings data
- Injury impact analysis
- Historical "games like this" comparisons
- Team momentum indicators (hot/cold streaks)

## 🙏 Acknowledgments

- Anthropic for creating MCP and Claude
- ESPN for providing public API access
- Sports fans everywhere who just want to know what to watch

---

**Built with ❤️ for sports fans who value their time**
