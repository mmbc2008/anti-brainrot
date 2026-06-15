# Anti-Brainrot

Anti-Brainrot is an event data pipeline that delivers personalised event updates to your Telegram account.

## Why this exists

I started this project because doomscrolling social media was wrecking my attention and mental health but quitting meant that I lost track of events that I actually cared about. After using [Hestia](https://github.com/wtfloris/hestia) for another use case, I realised a similar model could be used for event discovery, ergo anti-brainrot was born. [Check it out here on Telegram!](http://t.me/anti_brainrot_bot)

## How it works

1. The Linktree spider scrapes event organiser pages and discovers ticketing URLs, saving them as leads in a PostgreSQL database.
2. The Weeztix spider picks up pending leads, hits the OpenTicket API, and stores event data in the database.
3. The Telegram bot queries the database for new events and sends them directly to subscribers.


## Tech Stack
- **Scrapy**: web scraping and lead discovery
- **Scrapy-Playwright**: JavaScript-rendered page support
- **SQLite**: local event and subscriber storage
- **python-telegram-bot**: Telegram bot interface
- **uv**: Python package management

## Roadmap

- [ ] Add tests (unit tests for pipelines and spiders using pytest)
- [ ] Add more ticketing vendors (Eventbrite, fourvenues)
- [ ] dbt transformation layer for event data
- [ ] Prefect/Airflow orchestration to replace manual run order
- [ ] Filter events by category and location

## Contributing

Contributions are welcome, please see [CONTRIBUTING.md](./CONTRIBUTING.md) to find out how to get involved.

## License

Please see MIT [LICENSE](./LICENSE)