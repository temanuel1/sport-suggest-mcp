# Sport Suggest MCP

Your conversational AI sports companion that tells you what to watch right now.

> **🎯 The Problem:** You want to watch sports, but you don't know what's on or what's worth watching. Existing apps just show you schedules and scores - they don't understand what YOU want to watch right now.
>
> **💡 The Solution:** ESPN MCP turns Claude into your personal sports advisor. Have a conversation about what you're in the mood for, and get instant recommendations for the best games to watch - live right now or coming up soon.

## 🔥 What Makes This Different

**Traditional Sports Apps:**

- Show you everything that's on
- You have to manually browse through scores
- No understanding of what makes a game exciting
- Can't personalize to your mood or preferences

**ESPN MCP + Claude:**

- "Show me something exciting right now" → Claude finds close games, overtime, buzzer-beaters
- "I want to watch a game with playoff implications" → Claude analyzes standings and recommends
- "Find me a football game I can watch while working" → Claude suggests games early in the quarter
- "What should I watch this weekend?" → Claude reviews upcoming matchups and suggests the best ones

### Real Conversational Examples

**Right Now Recommendations:**

```
You: "I have 30 minutes, what should I watch?"

Claude: The Celtics-Lakers game is in the 4th quarter with 8 minutes
left and it's a 5-point game. Perfect timing - you'll catch the
entire finish. Plus it's a potential Finals preview.
```

**Future Planning:**

```
You: "What NFL games this Sunday are worth watching?"

Claude: Three games stand out:
1. Chiefs vs Bills (3pm) - AFC Championship rematch, both fighting
   for #1 seed
2. Cowboys vs Eagles (7pm) - Division rivals, loser is likely out
   of playoffs
3. 49ers vs Seahawks (7pm) - Winner takes division lead

Based on playoff implications, I'd prioritize Chiefs-Bills.
```

**Mood-Based Discovery:**

```
You: "I want to watch basketball but I'm tired of blowouts"

Claude: Right now there are 2 close games:
- Heat vs Bucks: 98-95, 6min left in 4th
- Nuggets vs Suns: Tied 103-103, 3min left in 4th

The Nuggets-Suns game is more exciting - they've had 8 lead
changes in the 4th quarter alone.
```

## 🚀 Why This Doesn't Exist Yet

**AI chatbots (ChatGPT, Claude, Gemini) cannot access live sports data.** They're completely blind to:

- What games are on right now
- Current scores and game situations
- Real-time player performances
- Playoff standings and implications

Apps like ESPN, Roku, and Samsung TV show you data, but they don't have conversations with you or understand your preferences in the moment.

**Sport Suggest MCP bridges this gap** - combining Claude's conversational intelligence with ESPN's live data to create a personalized sports discovery experience.

## 🛠️ How It Works

Sport Suggest MCP provides Claude with three powerful tools:

### 1. `get_live_games` - Find What's Exciting Right Now

Returns games currently in progress with smart filtering.

**What makes it smart:**

- Filter by score differential (close games only)
- Filter by game progress (4th quarter drama)
- Includes context: team records, playoff positioning
- TV broadcast info so you know where to watch

**Example:** "Show me NBA games in crunch time" → Only returns games in the 4th quarter within 10 points

---

### 2. `get_upcoming_games` - Plan Your Viewing

Get games scheduled for today, tomorrow, or any future date.

**What makes it smart:**

- Identifies playoff implications automatically
- Includes rivalry context and season series
- Shows team form (last 5 games)
- Highlights marquee matchups

**Example:** "What college football games Saturday have the biggest stakes?" → Returns ranked matchups with College Football Playoff implications

---

### 3. `get_game_details` - Deep Dive Analysis

Comprehensive breakdown of any specific game.

**What makes it smart:**

- Live stats and momentum indicators
- Key player performances
- Recent play-by-play highlights
- Injury reports
- Head-to-head history

**Example:** "Tell me about the Cowboys game" → Full analysis with score, stats, storylines, and whether it's worth tuning in

## 🎯 Perfect For These Scenarios

**"What should I watch right now?"**

- Finds the most exciting live games based on score, time remaining, and stakes
- Suggests multiple options if you have flexibility

**"What's on this weekend?"**

- Reviews all upcoming games and ranks by excitement factor
- Considers rivalries, playoff implications, star players

**"Find me a game I can put on in the background"**

- Suggests early-quarter games or blowouts you don't need to focus on
- Or finds nail-biters that demand your full attention

**"I only care about [my team], what should I know?"**

- Tracks your team's games and playoff positioning
- Alerts you to must-watch games

**"I want to watch basketball but I'm not sure which game"**

- Analyzes all live NBA games and suggests the best one
- Explains WHY it's worth watching

## 🏗️ Project Structure

```
sport-suggest-mcp/
├── src/
│   ├── index.ts              # MCP server setup
│   ├── tools/                # Tool implementations
│   │   ├── get_live_games.ts
│   │   ├── get_upcoming_games.ts
│   │   └── get_game_details.ts
│   ├── espn/                 # ESPN API client
│   │   ├── client.ts
│   │   └── types.ts
│   └── utils/                # Helper functions
│       ├── filters.ts
│       └── formatters.ts
├── package.json
├── tsconfig.json
└── README.md
```

## 📡 ESPN API Endpoints

This project uses ESPN's unofficial public API (no API key required):

```
Live scores:
http://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard

Game details:
http://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/summary?event={gameId}

Teams:
http://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/teams
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Claude Desktop
- Basic TypeScript knowledge

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sport-suggest-mcp.git
cd sport-suggest-mcp

# Install dependencies
npm install

# Build the project
npm run build
```

### Configuration

Add to your Claude Desktop config file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sport-suggest": {
      "command": "node",
      "args": ["/path/to/sport-suggest-mcp/build/index.js"]
    }
  }
}
```

Restart Claude Desktop, and you're ready to start discovering games!

## 🗺️ Development Roadmap

### Week 1: Core Discovery

- [ ] Initialize MCP server project
- [ ] Set up ESPN API client with error handling
- [ ] Implement `get_live_games` with basic filtering
- [ ] Test "what's on right now" queries

### Week 2: Smart Recommendations

- [ ] Add score differential and quarter filters to `get_live_games`
- [ ] Implement `get_upcoming_games` with date filtering
- [ ] Add playoff implications detection
- [ ] Test "what should I watch this weekend" queries

### Week 3: Deep Analysis

- [ ] Implement `get_game_details` for comprehensive breakdowns
- [ ] Add team form and head-to-head context
- [ ] Refine data formatting for conversational responses
- [ ] Test complex recommendation scenarios

### Week 4: Polish & Expand

- [ ] Comprehensive error handling
- [ ] Performance optimization
- [ ] Add more leagues (NHL, MLB, NCAAB)
- [ ] Documentation and examples

## 🎓 Key Design Philosophy

### Let Claude Be the Conversation Expert

We don't build rigid recommendation algorithms. Instead:

1. **We provide rich data** - scores, standings, team form, broadcast info
2. **Claude analyzes conversationally** - "This game is close AND has playoff implications AND features two MVP candidates"
3. **Recommendations feel natural** - like talking to a knowledgeable friend, not a database

### Context is Everything

Every game includes:

- **Stakes:** Playoff positioning, rivalry history, season series
- **Narrative:** Team streaks, player milestones, coaching storylines
- **Timing:** Quarter/inning, time remaining, momentum shifts
- **Accessibility:** What channel, when it starts, how long it'll take

This lets Claude understand not just WHAT is happening, but WHY it matters.

### Personalization Through Conversation

Instead of profile settings, preferences emerge naturally:

- "I love defense" → Claude prioritizes low-scoring, tight games
- "I'm a casual fan" → Claude explains context and storylines
- "I bet on this game" → Claude focuses on live scoring and momentum
- "I only have 20 minutes" → Claude finds games in the 4th quarter

## 📊 Success Metrics

- ✅ Recommend a relevant game in <2 seconds
- ✅ Understand conversational preferences ("exciting", "close", "important")
- ✅ Handle 5+ different leagues reliably
- ✅ Gracefully explain when nothing interesting is on
- ✅ Feel like talking to a knowledgeable sports friend

## 🔮 Future Enhancements

**Phase 2 - Advanced Discovery:**

- `get_player_stats` - "Is anyone having a monster game right now?"
- `get_standings` - Deep playoff scenario analysis
- Historical context - "Best game of the season so far"
- Betting line integration - "Which games are not going as expected?"

**Phase 3 - Proactive Suggestions:**

- "Heads up - the game you were watching is getting close again"
- "That team you mentioned is playing in 30 minutes"
- End-of-season scenarios - "Your team needs these 3 results to make playoffs"

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [ESPN API Unofficial Docs](https://gist.github.com/akeaswaran/b48b02f1c94f873c6655e7129910fc3b)

## 📝 License

MIT

## 🤝 Contributing

Contributions welcome! This is a learning project, but if you have ideas for making sports discovery even better, open an issue or PR.

**Ideas we'd love help with:**

- Additional sports (soccer, hockey, baseball)
- Better playoff implications detection
- Injury impact analysis
- Historical "games like this" comparisons

## 🙏 Acknowledgments

- Anthropic for creating MCP and Claude
- ESPN for providing public API access
- Sports fans everywhere who just want to know what to watch
