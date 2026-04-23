from urllib.parse import urlsplit, urljoin, urlparse
from bs4 import BeautifulSoup
import asyncio
import aiohttp
from abc import ABC, abstractmethod

class AsyncScraper(ABC):
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url 
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.base_domain = urlparse(self.base_url).netloc           
        self.page_data = {}                                         
        self.lock = asyncio.Lock()                                  
        self.semaphore = asyncio.Semaphore(self.max_concurrency)    
        self.session = None                                         
        self.should_stop = False
        self.all_tasks = set()
        self.source_types = ['weeztix', 'eventbrite', 'weticket']

    @abstractmethod
    def get_title_from_html(self, html):
        "The child class must implement this"
        
    @abstractmethod
    def get_date_from_html(self, html):
        "The child class must implement this"
        
    @abstractmethod
    def get_times_from_html(self, html):
        "The child class must implement this"
        
    @abstractmethod
    def get_location_from_html(self, html):
        "The child class must implement this"
        
    @abstractmethod
    def get_organiser_from_html(self, html):
        "The child class must implement this"
        
    @abstractmethod
    def get_category_from_html(self, html):
        "The child class must implement this"
        
    @abstractmethod
    def get_price_from_html(self, html):
        "The child class must implement this"
        
    
    def get_source_from_url(self, url):
        for source in self.source_types:
            if source in url:
                return source
            
    def find_source_from_outgoing_links(self, outgoing_links):
        sources_found = []
        found_source = ''
        for link in outgoing_links:
            sources_found.append(self.get_source_from_url(link))
        for source in sources_found:
            if source is not None:
                found_source = source
        return found_source
    
        
    def normalize_url(self, url):
        split_url = urlsplit(url.lower().strip('/'))
        return f"{split_url.netloc}{split_url.path}"

    def get_urls_from_html(self, html, base_url):
        urls = []
        soup = BeautifulSoup(html, 'html.parser')
        url_tags = soup.find_all('a', href=True)
        for tag in url_tags:
            urls.append(urljoin(base_url, tag.get('href')))
        return urls

    def get_base_url(self, url):
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}/"

    def extract_page_data(self, html, page_url):
        """_summary_

        Args:
            html (String): 
            page_url (String): is the absolute URL of the page (used for converting relative URLs)
            
        Returns:
            data (Dict): which contains the following keys; 
            url, event title, address, date, times, organiser name, category, price, outgoing links
            and the data from the html tags as values.
        """
        base_url = self.get_base_url(page_url)
        outgoing_links = self.get_urls_from_html(html, base_url)
        
        data = {
            'url': page_url,
            'event title': self.get_title_from_html(html),
            'address': self.get_location_from_html(html),
            'date': self.get_date_from_html(html),
            'times': self.get_times_from_html(html),
            'organiser name': self.get_organiser_from_html(html),
            'price': self.get_price_from_html(html),
            'outgoing_links': outgoing_links,
            'event_source': self.find_source_from_outgoing_links(outgoing_links)
        }
        return data
        
    async def __aenter__(self):
        """
        This function creates client sessions, which in turn allows you to make async HTTP requests.
        """
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc, tb):
        """
        This function closes the async http connections 
        Args:
            exc_type (type[BaseException]): exception type
            exc (BaseException): exception object
            tb (TracebackType): traceback
        """
        await self.session.close()
        
    async def add_page_visit(self, normalized_url):
        """
            Check if a page should be visited and mark it as pending.
            
            This function is thread-safe and handles:
            - Stopping the crawler if max_pages is reached
            - Preventing duplicate page visits
            - Thread-safe concurrent access with async lock
            
            Args:
                normalized_url (str): The normalized URL to check/add
                
            Returns:
                bool: True if URL is NEW and was added to queue
                    False if URL was already visited, max_pages reached, or crawler should stop
        """
        async with self.lock:
            if self.should_stop:
                return False
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to scrape.")
                for task in self.all_tasks:
                    task.cancel()
                return False
            if normalized_url in self.page_data:
                return False
            self.page_data[normalized_url] = None
            return True
        
    async def get_html(self, url):
        """
        Fetch HTML content from a URL with validation.
        
        Makes an async HTTP GET request to the provided URL and validates
        the response. Returns the HTML text only if:
        - Response status is < 400 (successful)
        - Content-Type header indicates HTML
        
        If validation fails or an error occurs, returns None instead of
        raising an exception (allows scraper to continue).
        
        Args:
            url (str): The URL to fetch HTML from
            
        Returns:
            str | None: The HTML content if successful, None if invalid
                    or error occurred
        """
        try: 
            async with self.session.get(url, headers={"User-Agent": "EventScraper/1.0"}) as response:
                if response.status >= 400:
                    print(f"Error: HTTP {response.status} for {url}")
                    return None
                elif 'text/html' not in response.headers.get('content-type', ""):
                    print(f"Error: Non-HTML content for {url}")
                    return None
                else:
                    response_text = await response.text()
                    return response_text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
        
    async def scrape_page(self, current_url):
        """
        Recursively scrape a page and all linked pages within the same domain.
        
        Fetches HTML, extracts page data, finds new URLs, and creates async tasks
        to scrape them. Uses semaphore for concurrency limits and lock for thread-safety.
        
        Args:
            current_url (str): The URL to scrape
            
        Returns:
            None: Results stored in self.page_data
        """
        if self.should_stop:
            return 
        if urlparse(current_url).netloc != self.base_domain:
            return 
            
        normalized_url = self.normalize_url(current_url)
        # Call and await your new add_page_visit method, if it is not a new page return early
        is_new = await self.add_page_visit(normalized_url)
        if not is_new:
            return 
        # Use async with self.semaphore to limit the number of concurrent requests
        async with self.semaphore:
            # Fetch the page's HTML and extract page data using extract_page_data
            html = await self.get_html(current_url)
            if html is None:
                return 
            new_data = self.extract_page_data(html, normalized_url)
            # Add the page data to page_data dictionary using the normalized URL as the key (use the lock to do this safely)
            async with self.lock:
                self.page_data[normalized_url] = new_data 
        # Extract new URLs from the page
        new_urls = self.get_urls_from_html(html, self.base_url)
        # For each URL, create a task to crawl it using asyncio.create_task
        background_tasks = set()
        for url in new_urls:
            task = asyncio.create_task(self.scrape_page(url))
            background_tasks.add(task)
            self.all_tasks.add(task)
        # Wait for all tasks with await asyncio.gather(*tasks)
        try: 
            await asyncio.gather(*background_tasks, return_exceptions=True)
        finally:
            for task in background_tasks:
                self.all_tasks.discard(task)
    
    async def scrape(self, max_con, max_pages):
        """
        Entry point for the crawler. Updates concurrency/page limits and starts scraping.
        
        Initiates the recursive scraping process starting from self.base_url.
        The actual crawling happens in scrape_page(), which runs asynchronously
        and recursively crawls all linked pages within the same domain.
        
        Args:
            max_con (int): Maximum concurrent HTTP requests allowed
            max_pages (int): Maximum number of pages to scrape before stopping
            
        Returns:
            dict: Dictionary of all scraped page data keyed by normalized URL
        """
        self.max_concurrency = max_con
        await self.scrape_page(self.base_url)
        self.max_pages = max_pages
        filtered_data = { key: value for key, value in self.page_data.items() if value is not None}
        return filtered_data
    
    