import sys
import asyncio
from linktree_scraper import scrape_site_async


async def main():
    BASE_URL = sys.argv[1]
    MAX_CONCURRENCY = int(sys.argv[2])
    MAX_PAGES = int(sys.argv[3])
    print("Starting scrape of: ", BASE_URL)
    page_data = await scrape_site_async(BASE_URL, MAX_CONCURRENCY, MAX_PAGES)
    print(f"There are {len(page_data)} that pages have been scraped.")
    print(page_data)
    
if __name__ == "__main__":
    asyncio.run(main())