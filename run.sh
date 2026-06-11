#!/bin/bash
cd scraper
uv run scrapy crawl linktree
uv run scrapy crawl weeztix
cd ..
uv run python bot/notifier.py