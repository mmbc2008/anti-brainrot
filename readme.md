# Anti-Brainrot

Anti-Brainrot is an event aggregator that delivers personalised event updates to your messaging app of choice. Currently shipping a Telegram bot interface; designed to support Signal, and Discord.





## Setup

This project uses [uv](https://docs.astral.sh/uv/) for Python package management.

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repo
git clone https://github.com/your-actual-username/anti-brainrot.git
cd anti-brainrot

# Sync dependencies (creates .venv and installs from uv.lock)
uv sync

# Install Playwright browsers
uv run playwright install
```
## Why this exists

I started this project because doomscrolling social media was wrecking my attention and mental health but quitting meant that I lost track of events that I actually cared about. After using [Hestia](https://github.com/wtfloris/hestia) for another use case, I realised a similar model could be used for event discovery, ergo anti-brainrot was born. 