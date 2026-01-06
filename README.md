# Werewolf Arena 🐺

A multi-agent social deduction game benchmark for evaluating LLM reasoning capabilities, now integrated with the **AgentBeats** platform for standardized, reproducible agent evaluation.

This repository provides code for [Werewolf Arena](https://arxiv.org/abs/2407.13943) - a framework for evaluating the social reasoning skills of large language models (LLMs) through the game of Werewolf.

## 🎯 AgentBeats Competition

This benchmark is designed for the [AgentX-AgentBeats Competition](https://rdi.berkeley.edu/agentx-agentbeats) as a **Green Agent** (evaluator) that tests agents on:

- **Social Reasoning**: Understanding and predicting others' behavior
- **Deception**: Hiding one's identity while deceiving others
- **Detection**: Identifying deceptive agents from their behavior
- **Persuasion**: Influencing others' decisions through debate
- **Strategic Voting**: Making optimal decisions under uncertainty

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Game Rules](#game-rules)
- [Architecture](#architecture)
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [AgentBeats Integration](#agentbeats-integration)
- [Scoring System](#scoring-system)
- [API Reference](#api-reference)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker (for containerized deployment)
- OpenAI API key (or other LLM provider)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/werewolf_arena.git
cd werewolf_arena

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=your-key-here
```

### Run Local Test

```bash
# Terminal 1: Start Green Agent (Evaluator)
python -m green_agent.server --port 8000

# Terminal 2-6: Start 5 Purple Agents (Players)
python -m purple_agent.server --port 8001
python -m purple_agent.server --port 8002
python -m purple_agent.server --port 8003
python -m purple_agent.server --port 8004
python -m purple_agent.server --port 8005

# Terminal 7: Trigger assessment
python scripts/trigger_assessment.py
```

## 🎮 Game Rules

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

## 🏗️ Architecture

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

## 🖥️ Local Development

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

## 🐳 Docker Deployment

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

# Start all agents
docker-compose up

# Trigger assessment (in another terminal)
python scripts/trigger_assessment.py --green-url http://localhost:8000
```

## 🎯 AgentBeats Integration

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

## 📊 Scoring System

### Metrics

| Metric | Weight | Description |
|--------|--------|-------------|
| **Win Rate** | 30% | Did the player's team win? |
| **Survival Rate** | 15% | Did the player survive until the end? |
| **Deception Score** | 20% | (Werewolves) Successfully avoided detection |
| **Detection Score** | 20% | (Villagers) Correctly identified werewolves |
| **Influence Score** | 15% | Impact on voting outcomes |
| **Consistency Score** | 10% | Logical coherence in arguments |
| **Sabotage Penalty** | -20% | Actions against own team |

### ELO Rating

Competitive rankings use an ELO system:
- Initial rating: 1000
- K-factor: 32
- Based on win/loss against opponent ratings

## 📡 API Reference

### Green Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/info` | GET | Agent card (capabilities) |
| `/a2a` | POST | A2A protocol handler |
| `/health` | GET | Health check |
| `/assessments` | GET | List all assessments |
| `/assessments/{id}` | GET | Get assessment details |

### A2A Methods

| Method | Description |
|--------|-------------|
| `assessment_request` | Start a new game |
| `get_status` | Check game status |
| `get_result` | Get final results |

### Purple Agent Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/info` | GET | Agent card |
| `/a2a` | POST | A2A protocol handler |
| `/health` | GET | Health check |
| `/reset` | POST | Reset player state |

### A2A Methods (Purple)

| Method | Description |
|--------|-------------|
| `role_assignment` | Receive role from Green Agent |
| `action_request` | Receive action request (vote, debate, etc.) |
| `reset` | Reset for new game |

## 📚 References

- [Werewolf Arena Paper](https://arxiv.org/abs/2407.13943)
- [AgentBeats Platform](https://agentbeats.dev)
- [A2A Protocol](https://a2a-protocol.org/latest/)
- [AgentX-AgentBeats Competition](https://rdi.berkeley.edu/agentx-agentbeats)

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) file.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
