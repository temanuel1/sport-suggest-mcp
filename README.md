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

### Real Conversational Examples

**Right Now Recommendations:**

```
You: "What's the most exciting NFL game on right now?"

Claude: The Bengals-Jets game is your best bet - it's 38-32 with
4:36 left in the 4th quarter. That's a 6-point game with enough
time for a comeback, and the pace is insane at 17.5 points per
quarter. Plus it's on CBS.
```

**Style-Based Discovery:**

```
You: "I want a defensive battle"

Claude: The Bucs-Saints game is perfect for you. It's 7-3 in the
3rd quarter with a pace of only 3.3 points per period. Both teams
are struggling to move the ball, and the Superdome crowd is into it.
```

**Mood-Based Discovery:**

```
You: "I'm new to basketball, what should I watch?"

Claude: I'd suggest the Lakers-Celtics game - it's a historic
rivalry between two legendary franchises. LeBron James is having
a monster game with 35 points, and it's close enough (8-point game)
that you'll see competitive basketball without a blowout. Plus
you'll learn about two of the best teams in the league.
```

**Player Performance Focus:**

```
You: "Any star performances happening right now?"

Claude: Yes! In the Broncos-Cowboys game, RJ Harvey already has
2 rushing touchdowns and Troy Franklin has 74 receiving yards and
a TD. The Broncos are rolling, and Bo Nix is having a great game
as a young QB. Worth tuning in to see the future stars.
```

## 🚀 Why This Doesn't Exist Yet

**AI chatbots (ChatGPT, Claude, Gemini) cannot access live sports data.** They're completely blind to:

- What games are on right now
- Current scores and game situations
- Real-time player performances
- Game pace and momentum

Apps like ESPN, Roku, and Samsung TV show you data, but they don't have conversations with you or understand your preferences in the moment.

**Sport Suggest MCP bridges this gap** - combining Claude's conversational intelligence with ESPN's live data to create a personalized sports discovery experience.

## 🛠️ How It Works

Sport Suggest MCP provides Claude with two powerful tools that return rich, structured data. Claude then analyzes this data conversationally to understand what YOU want to watch.

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

This approach is infinitely flexible - as your preferences evolve in the conversation, Claude adapts without any code changes.

## 🏗️ Project Structure

```
sport-suggest-mcp/
├── src/
│   └── sport_suggest_mcp/
│       ├── __init__.py
│       ├── server.py           # MCP server setup & tool registration
│       └── tools.py            # get_nfl_scores & get_nba_scores implementations
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

**Data returned includes:**

- Live scores and game status (quarter, time remaining)
- Team information (names, records, abbreviations)
- Statistical leaders (top performers for each team)
- Venue and broadcast details
- Quarter-by-quarter scoring breakdowns

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

### Player-Focused

- "Any star performances happening?"
- "Who's having a monster game?"
- "Show me games with great QB play"
- "Are there any players going off right now?"

### Team-Based

- "Should I watch the Cowboys game?"
- "Show me games with winning teams"
- "Find me a good matchup"
- "Any rivalry games on?"

### Upcoming Games

- "What NFL games are coming up tonight?"
- "What should I watch this weekend?"
- "When does the Lakers game start?"

## 🗺️ Development Roadmap

### ✅ Phase 1: Core Discovery (Complete)

- [x] MCP server setup with Python
- [x] ESPN API client with NFL & NBA support
- [x] `get_nfl_scores` with rich player/game data
- [x] `get_nba_scores` with rich player/game data
- [x] Filtering out completed games
- [x] Real-time player performance tracking

### 🚧 Phase 2: Enhanced Intelligence (In Progress)

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

1. **We provide rich data** - scores, player stats, pace metrics, team records
2. **Claude analyzes conversationally** - "This game is close AND has a high pace AND features star performers"
3. **Recommendations feel natural** - like talking to a knowledgeable friend, not querying a database

### Data-Driven But Not Prescriptive

Every game includes enough context for Claude to make intelligent recommendations:

- **Stakes:** Team records, conference games
- **Style:** Pace metrics, scoring patterns, defensive vs offensive battles
- **Talent:** Player performance leaders (QB/RB/WR for NFL, PTS/REB/AST for NBA)
- **Timing:** Quarter/time remaining, halftime, upcoming
- **Accessibility:** Broadcast channel, venue, attendance

This lets Claude understand not just WHAT is happening, but WHY it matters to YOU.

### Personalization Through Conversation

Instead of profile settings, preferences emerge naturally through dialogue:

- "I love defense" → Claude prioritizes low-pace, close games
- "I'm a casual fan" → Claude explains context and storylines
- "I only have 20 minutes" → Claude finds games in the 4th quarter
- "Show me star power" → Claude highlights games with top statistical performances

## 📊 Success Metrics

- ✅ Recommend a relevant game in <2 seconds
- ✅ Understand conversational preferences ("exciting", "close", "high-scoring")
- ✅ Handle NFL and NBA reliably with live data
- ✅ Gracefully explain when nothing interesting is on
- ✅ Feel like talking to a knowledgeable sports friend

## 🔧 Technical Details

### Why Python?

- Simple, readable code for sports data parsing
- Excellent support for REST APIs via `requests`
- Fast development iteration
- Easy integration with MCP Python SDK

### Why Two Separate Tools?

We initially considered a single `get_league_scores(league)` router function, but decided on separate `get_nfl_scores()` and `get_nba_scores()` tools because:

1. **Simpler for Claude** - Direct function calls vs parameter passing
2. **Sport-specific logic** - NFL uses QB/RB/WR leaders, NBA uses PTS/REB/AST
3. **Easier to extend** - Add `get_mlb_scores()` later without touching existing code
4. **Better performance** - No unnecessary routing layer

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

Our tool functions handle these differences internally, presenting clean, consistent data to Claude.

## 🐛 Known Issues & Limitations

- **Attendance data is unreliable** - ESPN doesn't always populate it, even for live games
- **Halftime detection** - Some edge cases during halftime transitions
- **Season stats vs game stats** - For upcoming games, API sometimes returns season totals instead of game stats (we filter these out)

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [ESPN API Unofficial Docs](https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b)

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! This is a learning project exploring the intersection of AI and sports discovery.

**Ideas we'd love help with:**

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
