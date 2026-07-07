<img width="2172" height="724" alt="c018851c-4b63-4a3b-b606-3d1d20400a11" src="https://github.com/user-attachments/assets/8b624426-df9b-48a9-aeba-77fe359c3ae2" />

# Z Agent — Autonomous Solana KOL Bot

An AI-powered Twitter/X reply bot that roleplays as a Solana alpha-caller. Built with Python, xAI's Grok API, and the Twitter v2 API.

## Overview

Z Agent is an autonomous bot that monitors Twitter mentions and generates contextual replies in the style of a high-conviction Solana trader/KOL. It uses Grok's language model for response generation with multiple fallback strategies to ensure consistent output.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Z AGENT SYSTEM                   │
├─────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Twitter  │───▶│   Core   │───▶│   xAI    │  │
│  │  Poller   │    │  Engine  │    │  Grok    │  │
│  └──────────┘    └──────────┘    └──────────┘  │
│       │                │                │        │
│       ▼                ▼                ▼        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Mention  │    │  Context │    │ Response  │  │
│  │ Detection │    │ Builder  │    │ Generator │  │
│  └──────────┘    └──────────┘    └──────────┘  │
│                                                   │
│  ┌──────────────────────────────────────────┐   │
│  │           Deduplication Layer              │   │
│  │        (replied_ids.json persistence)     │   │
│  └──────────────────────────────────────────┘   │
│                                                   │
└─────────────────────────────────────────────────┘
```

## Features

- **Real-time mention monitoring** via Twitter v2 Search API
- **Context-aware replies** — fetches parent tweets for threaded conversations
- **Multi-strategy response generation:**
  - Primary prompt (full character + context)
  - Fallback prompt (softer framing for edge cases)
  - Hardcoded responses (guaranteed output)
- **Refusal detection** — automatically retries with alternative prompts if AI hedges
- **Deduplication** — persistent storage of replied tweet IDs (survives restarts)
- **Rate limiting** — configurable polling intervals with jitter

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| AI Model | xAI Grok (grok-4-1-fast-reasoning) |
| Twitter API | v2 (OAuth 1.0a + Bearer) |
| Persistence | JSON file-based |
| Auth | OAuth1 (requests-oauthlib) |

## File Structure

```
zagentics/
├── bot.py                 # Main bot entry point
├── config.py              # Configuration & environment variables
├── prompts/
│   ├── primary.txt        # Primary system prompt
│   └── fallback.txt       # Fallback system prompt
├── core/
│   ├── __init__.py
│   ├── twitter.py         # Twitter API interactions
│   ├── ai.py              # xAI/Grok response generation
│   ├── context.py         # Tweet context builder
│   └── dedup.py           # Deduplication persistence
├── data/
│   └── replied_ids.json   # Replied tweet ID store
├── requirements.txt
├── .env.example
├── Dockerfile
└── README.md
```

## Installation

```bash
git clone https://github.com/zagentics/z-agent.git
cd z-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your credentials
python bot.py
```

## Configuration

All configuration is done via environment variables. Copy `.env.example` to `.env` and fill in your values:

```env
# Twitter API v2
TWITTER_CONSUMER_KEY=your_consumer_key
TWITTER_CONSUMER_SECRET=your_consumer_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

# xAI (Grok)
XAI_API_KEY=your_xai_api_key
XAI_MODEL=grok-4-1-fast-reasoning

# Bot Config
BOT_USERNAME=zagentics
POLL_INTERVAL=30
TEMPERATURE=0.9
MAX_REPLY_LENGTH=280
```

## How It Works

### 1. Polling Loop

The bot polls Twitter's Recent Search endpoint every ~30 seconds for new mentions of `@zagentics`. A random jitter of ±5 seconds prevents predictable request patterns.

### 2. Context Building

For reply mentions, the bot fetches the parent tweet to understand the full conversation context. This allows contextually relevant responses rather than replying in a vacuum.

### 3. Response Generation

```python
# Three-tier response strategy
1. Primary prompt + full context → Grok API
2. If refusal detected → Fallback prompt + simplified context → Grok API
3. If both fail → Hardcoded fallback reply (always succeeds)
```

### 4. Refusal Detection

The bot scans AI responses for hedging phrases like "as an AI", "I can't", "not comfortable", etc. If detected, it automatically retries with a softer prompt framing.

### 5. Deduplication

Every successfully replied tweet ID is persisted to `replied_ids.json`. On restart, the bot loads this file to avoid double-replying.

## Response Style

The bot generates short, conviction-based replies typical of Solana CT culture:

- Brief (usually under 100 characters)
- Confident, not verbose
- Narrative-driven market commentary
- Alpha-dropping energy
- No hashtags, minimal emojis

## Rate Limits

| Resource | Limit | Bot Usage |
|----------|-------|-----------|
| Search/recent | 180 req/15min | ~30 req/15min |
| Post tweet | 200 req/15min | Variable (1 per mention) |
| xAI API | Per plan | ~2-3 calls per mention |

## Deployment

### Local

```bash
python bot.py
```

### Docker

```bash
docker build -t z-agent .
docker run -d --env-file .env --name z-agent z-agent
```

### Systemd (Linux)

```ini
[Unit]
Description=Z Agent Bot
After=network.target

[Service]
Type=simple
User=bot
WorkingDirectory=/opt/z-agent
ExecStart=/opt/z-agent/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Error Handling

- **Twitter API failures**: Logged and retried after 60s cooldown
- **xAI API failures**: Falls through to next prompt strategy
- **Network timeouts**: 10-25s timeouts with graceful degradation
- **Deduplication corruption**: Graceful fallback to empty set

## Monitoring

The bot outputs structured logs to stdout:

```
Ansem (Z) agent starting...
Monitoring @zagentics
Bearer token OK
Loaded 142 replied IDs from disk.
Using polling fallback (every ~30s)
New mention from @user123: what's the play right now?
Attempt 1: primary prompt...
→ Ansem: sol looks ready. narrative forming and nobody is paying attention yet
Replied to 1234567890
```

## License

MIT

## Disclaimer

This is an experimental AI bot for research and entertainment purposes. It does not provide financial advice. All generated content is AI-produced and should not be taken as investment guidance.
