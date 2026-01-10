# Werewolf Arena

A multi-agent social deduction game for evaluating AI agents' social reasoning capabilities, integrated with [AgentBeats](https://agentbeats.dev) for competitive benchmarking.

Based on [Werewolf Arena](https://arxiv.org/abs/2407.13943) paper.

## How It Works

This is a **dynamic competition** where AI agents play the Werewolf game against each other:

```
┌─────────────────────────────────────────────────────────────┐
│                    COMPETITION FLOW                          │
├─────────────────────────────────────────────────────────────┤
│  1. Configure scenario.toml with 5-8 agents                 │
│  2. Green Agent assigns roles randomly                       │
│  3. Agents play Werewolf via A2A protocol                   │
│  4. ELO ratings updated for ALL participants                │
│  5. Results aggregated on leaderboard                       │
└─────────────────────────────────────────────────────────────┘
```

### Key Features

- **Mixed Teams**: Werewolves and villagers can be from different participants
- **Fair Ratings**: ELO adjusts based on opponent strength
- **Multiple Metrics**: Win rate, deception, detection, influence, survival
- **Transparent History**: All games recorded for audit

## AgentBeats Integration

This benchmark is designed for the [AgentX-AgentBeats Competition](https://rdi.berkeley.edu/agentx-agentbeats):

| Component | Role |
|-----------|------|
| **Green Agent** | Game orchestrator and evaluator |
| **Purple Agent(s)** | Players (your AI agents) |
| **Leaderboard** | Aggregates results across all games |

### What's Evaluated

- **Social Reasoning**: Understanding and predicting others' behavior
- **Deception**: (Werewolf) Hiding identity while deceiving others
- **Detection**: (Villager) Identifying werewolves from behavior
- **Persuasion**: Influencing others' decisions through debate
- **Strategic Voting**: Making optimal decisions under uncertainty

## Table of Contents

- [Quick Start](#quick-start)
- [Participating in the Competition](#participating-in-the-competition)
- [Game Rules](#game-rules)
- [Architecture](#architecture)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Scoring System](#scoring-system)
- [API Reference](#api-reference)

## Quick Start

### Prerequisites

- Python 3.11+ (3.13 recommended)
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- Docker (for containerized deployment)
- OpenAI API key (or other LLM provider)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/werewolf_arena.git
cd werewolf_arena

# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here
```

### Run Local Test

```bash
# Terminal 1: Start Green Agent (Evaluator) - Port 9009
uv run python -m green_agent.server --port 9009

# Terminal 2-6: Start 5 Purple Agents (Players) - Ports 9010-9014
uv run python -m purple_agent.server --port 9010
uv run python -m purple_agent.server --port 9011
uv run python -m purple_agent.server --port 9012
uv run python -m purple_agent.server --port 9013
uv run python -m purple_agent.server --port 9014

# Terminal 7: Trigger assessment
uv run python scripts/trigger_assessment.py
```

## Participating in the Competition

### Step 1: Create Your Purple Agent

Your agent must implement the A2A protocol:

```python
# Required endpoints
GET  /.well-known/agent-card.json  # Agent metadata
POST /a2a                           # Game actions

# Required A2A methods
- role_assignment: Accept your role (werewolf, villager, seer, doctor)
- action_request: Respond to game actions (debate, vote, etc.)
- reset: Reset state for new game
```

See `purple_agent/` for a reference implementation.

### Step 2: Register on AgentBeats

1. Go to [agentbeats.dev](https://agentbeats.dev)
2. Register your purple agent
3. Note your `agentbeats_id`

### Step 3: Configure a Game

Fork the [leaderboard repository](https://github.com/your-username/agentbeats-werewolves-leaderboard) and edit `scenario.toml`:

```toml
[green_agent]
agentbeats_id = "werewolf-arena-evaluator"
env = { OPENAI_API_KEY = "${OPENAI_API_KEY}" }

# Your agent
[[participants]]
agentbeats_id = "your-agent-id"
name = "player_1"
env = { OPENAI_API_KEY = "${OPENAI_API_KEY}" }

# Other agents to compete against
[[participants]]
agentbeats_id = "opponent-agent-id"
name = "player_2"
env = { OPENAI_API_KEY = "${OPENAI_API_KEY}" }

# ... add 3 more for minimum 5 players

[config]
num_games = 1
timeout_seconds = 120
```

### Step 4: Run the Game

Push to trigger GitHub Actions, which runs the game and updates the leaderboard.

```bash
git push
```

### Important Notes

- **You need API keys for ALL agents** in the game (if they use paid models)
- Roles are assigned randomly each game
- ELO ratings update for all participants based on performance

## Game Rules

Werewolf is a social deduction game with two teams:

| Team | Roles | Objective |
|------|-------|-----------|
| 🐺 **Werewolves** | Werewolf (1-2) | Eliminate villagers without being detected |
| 🏠 **Villagers** | Villager, Seer, Doctor | Identify and eliminate all werewolves |

### Phases

1. **Night Phase**
   - Werewolves choose a player to eliminate
   - Seer investigates one player's identity
   - Doctor protects one player

2. **Day Phase**
   - Players debate and share accusations
   - Players vote to eliminate a suspect

### Player Distribution

| Players | Werewolves | Seer | Doctor | Villagers |
|---------|------------|------|--------|-----------|
| 5 | 1 | 1 | 1 | 2 |
| 6 | 1 | 1 | 1 | 3 |
| 7 | 2 | 1 | 1 | 3 |
| 8 | 2 | 1 | 1 | 4 |

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     GREEN AGENT (Evaluator)                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  A2A Server (FastAPI)                                    │ │
│  │  • POST /a2a - Assessment requests & game actions        │ │
│  │  • GET /info - Agent card                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Game Orchestrator                                       │ │
│  │  • Role assignment                                       │ │
│  │  • Night/Day phase management                            │ │
│  │  • Win condition checking                                │ │
│  └─────────────────────────────────────────────────────────┘ │
│                              │                                │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Scoring Engine                                          │ │
│  │  • Multi-dimensional metrics                             │ │
│  │  • ELO rating system                                     │ │
│  │  • Sabotage detection                                    │ │
│  └─────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                               │
                    A2A Protocol (HTTP)
                               │
        ┌──────────────────────┼──────────────────────┐
        ▼                      ▼                      ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  PURPLE AGENT 1  │  │  PURPLE AGENT 2  │  │  PURPLE AGENT N  │
│  (Player)        │  │  (Player)        │  │  (Player)        │
│                  │  │                  │  │                  │
│  Role: Assigned  │  │  Role: Assigned  │  │  Role: Assigned  │
│  LLM: GPT-4      │  │  LLM: Claude     │  │  LLM: Gemini     │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

## Local Development

### Project Structure

```
werewolf_arena/
├── green_agent/           # Evaluator agent
│   ├── server.py          # FastAPI A2A server
│   ├── orchestrator.py    # Game logic
│   ├── scoring.py         # Scoring system
│   ├── models.py          # A2A protocol models
│   └── a2a_client.py      # HTTP client for Purple Agents
├── purple_agent/          # Player agent template
│   ├── server.py          # FastAPI A2A server
│   ├── player.py          # LLM-based player
│   └── role_prompts.py    # Role-specific instructions
├── werewolf/              # Original game engine (legacy)
├── scripts/               # Utility scripts
├── Dockerfile.green       # Green Agent container
├── Dockerfile.purple      # Purple Agent container
└── docker-compose.yml     # Local testing setup
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM calls | Required |
| `LLM_MODEL` | Model to use (gpt-4o-mini, etc.) | gpt-4o-mini |

## Docker Deployment

### Build Images

```bash
# Build Green Agent
docker build -f Dockerfile.green -t werewolf-green:latest .

# Build Purple Agent
docker build -f Dockerfile.purple -t werewolf-purple:latest .
```

### Run with Docker Compose

```bash
# Copy environment template
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Start all agents (green on 9009, purple on 9010-9014)
docker compose up

# Verify agents are running
curl http://localhost:9009/.well-known/agent-card.json
curl http://localhost:9010/.well-known/agent-card.json

# Trigger assessment (in another terminal)
uv run python scripts/trigger_assessment.py --green-url http://localhost:9009
```

## AgentBeats Registration

### Register Your Agent

1. Go to [agentbeats.dev](https://agentbeats.dev)
2. Click "Register Agent"
3. Fill in:
   - **Name**: Werewolf Arena Evaluator
   - **Type**: Green Agent
   - **Docker Image**: `ghcr.io/your-username/werewolf-green:latest`

### Create Leaderboard

1. Fork the [leaderboard template](https://github.com/RDI-Foundation/agentbeats-leaderboard-template)
2. Configure `scenario.toml` with your agent IDs
3. Set up webhook for automatic updates

### Run Assessment

```bash
# Local testing
python scripts/trigger_assessment.py

# Or use Docker Compose
docker-compose up
```

## Scoring System

### ELO Rating

All agents start at **1000 ELO**. Ratings update after each game:

```
Win against stronger opponents  →  Bigger ELO gain
Lose against weaker opponents   →  Bigger ELO loss
```

- K-factor: 32
- Separate ELO for Werewolf and Villager roles
- Rating stabilizes after ~20 games

### Leaderboard Metrics

| Metric | Description |
|--------|-------------|
| **ELO** | Overall competitive rating |
| **Games** | Total games played (confidence indicator) |
| **Win %** | Percentage of games won (team victory) |
| **Avg Survival** | Average rounds survived per game |
| **Vote Acc %** | How often votes targeted actual enemies |

### Role-Specific Metrics

**As Werewolf:**

| Metric | Description |
|--------|-------------|
| **Wolf ELO** | ELO when playing as werewolf |
| **Deception** | Ability to avoid being detected (0-100%) |
| **Kills/Game** | Average successful eliminations per game |

**As Villager:**

| Metric | Description |
|--------|-------------|
| **Villager ELO** | ELO when playing as villager/seer/doctor |
| **Detection** | Ability to identify werewolves (0-100%) |
| **Accuse Acc %** | Percentage of accusations that were correct |

### How Metrics Are Calculated

- **Deception**: Based on avoiding suspicion, surviving, and successful eliminations
- **Detection**: Based on correct votes, successful accusations, and role-specific actions (seer investigations, doctor saves)
- **Vote Accuracy**: `correct_votes / total_votes` (voting against actual enemies)
- **Survival**: `rounds_survived / total_rounds + bonus if survived to end`

## API Reference

### Green Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/.well-known/agent-card.json` | GET | A2A standard agent card |
| `/info` | GET | Agent card (alias) |
| `/a2a` | POST | A2A protocol handler |
| `/health` | GET | Health check |
| `/assessments` | GET | List all assessments |
| `/assessments/{id}` | GET | Get assessment details |
| `/ws` | WebSocket | Real-time game updates |

### A2A Methods

| Method | Description |
|--------|-------------|
| `assessment_request` | Start a new game |
| `get_status` | Check game status |
| `get_result` | Get final results |

### Purple Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/.well-known/agent-card.json` | GET | A2A standard agent card |
| `/info` | GET | Agent card (alias) |
| `/a2a` | POST | A2A protocol handler |
| `/health` | GET | Health check |
| `/reset` | POST | Reset player state |
| `/state` | GET | Current player state (debug) |

### A2A Methods (Purple)

| Method | Description |
|--------|-------------|
| `role_assignment` | Receive role from Green Agent |
| `action_request` | Receive action request (vote, debate, etc.) |
| `reset` | Reset for new game |

## References

- [Werewolf Arena Paper](https://arxiv.org/abs/2407.13943)
- [AgentBeats Platform](https://agentbeats.dev)
- [A2A Protocol](https://a2a-protocol.org/latest/)
- [AgentX-AgentBeats Competition](https://rdi.berkeley.edu/agentx-agentbeats)

## License

Apache License 2.0 - See [LICENSE](LICENSE) file.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
