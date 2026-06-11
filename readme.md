# Anti-Brainrot

Anti-Brainrot is an event aggregator that delivers personalised event updates to your messaging app of choice. Currently shipping a Telegram bot interface.
## Why this exists

I started this project because doomscrolling social media was wrecking my attention and mental health but quitting meant that I lost track of events that I actually cared about. After using [Hestia](https://github.com/wtfloris/hestia) for another use case, I realised a similar model could be used for event discovery, ergo anti-brainrot was born. 

## How it works

1. The Linktree spider scrapes event organiser pages and discovers ticketing URLs, saving them as leads in a local SQLite database.
2. The Weeztix spider picks up pending leads, hits the OpenTicket API, and stores event data in the database.
3. The Telegram bot queries the database for new events and sends them directly to subscribers.


## Tech Stack
- **Scrapy**: web scraping and lead discovery
- **Scrapy-Playwright**: JavaScript-rendered page support
- **SQLite**: local event and subscriber storage
- **python-telegram-bot**: Telegram bot interface
- **uv**: Python package management

## Setup

This project uses [uv](https://docs.astral.sh/uv/) for Python package management. Running `uv sync` will install all dependencies automatically from `uv.lock` no need to install packages individually.

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repo
git clone https://github.com/mmbc2008/anti-brainrot
cd anti-brainrot

# Sync dependencies (creates .venv and installs from uv.lock)
uv sync

# Install Playwright browsers
uv run playwright install

# Create a Telegram bot and get your token via @BotFather on Telegram
# See: https://core.telegram.org/bots/tutorial#obtain-your-bot-token

# Copy the example env file and add your Telegram bot token
cp .env.example .env

# Seed the database
uv run python seed.py
```

## Usage

Run the spiders from the `scraper/` directory:

```bash
cd scraper
uv run scrapy crawl linktree
uv run scrapy crawl weeztix
```

Then run the bot from the project root:

```bash
cd ..
uv run python bot/notifier.py
```

Or run everything at once from the project root:

```bash
bash run.sh
```

## Roadmap

- [ ] Add tests (unit tests for pipelines and spiders using pytest)
- [ ] Add more ticketing vendors (Eventbrite, fourvenues)
- [ ] dbt transformation layer for event data
- [ ] Prefect/Airflow orchestration to replace manual run order
- [ ] Filter events by category and location
- [ ] Signal and Discord bot interfaces
- [ ] Deploy for 24/7 running on a Linux VPS (Hetzner) / Railway and Fly.io also supported for a quicker setup

## Contributing

Contributions are welcome, please see [CONTRIBUTING.md](./CONTRIBUTING.md) to find out how to get involved.

## License

Please see MIT [LICENSE](./LICENSE)