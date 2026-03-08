import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from config import MAX_CONCURRENT_REQUESTS, DELAY_BETWEEN_REQUESTS, TIMEOUT
from src.utils import get_random_user_agent
import logging

logger = logging.getLogger(__name__)

class Crawler:
    def __init__(self, base_url, max_depth=3):
        self.base_url = base_url
        self.max_depth = max_depth
        self.visited = set()
        self.to_visit = asyncio.Queue()
        self.session = None
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        self.found_urls = set()
        self.js_files = []

    async def crawl(self):
        """Start crawling from base_url."""
        await self.to_visit.put((self.base_url, 0))
        async with aiohttp.ClientSession(
            headers={'User-Agent': get_random_user_agent()},
            timeout=aiohttp.ClientTimeout(total=TIMEOUT)
        ) as session:
            self.session = session
            tasks = []
            for _ in range(MAX_CONCURRENT_REQUESTS):
                task = asyncio.create_task(self._worker())
                tasks.append(task)
            await self.to_visit.join()
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _worker(self):
        while True:
            try:
                url, depth = await self.to_visit.get()
                if url in self.visited or depth > self.max_depth:
                    self.to_visit.task_done()
                    continue
                self.visited.add(url)
                await self._fetch(url, depth)
                self.to_visit.task_done()
                await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error crawling {url}: {e}")
                self.to_visit.task_done()

    async def _fetch(self, url, depth):
        async with self.semaphore:
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        self.found_urls.add(url)
                        soup = BeautifulSoup(content, 'lxml')
                        # Extract links
                        for link in soup.find_all('a', href=True):
                            next_url = urljoin(url, link['href'])
                            if self._is_same_domain(next_url):
                                await self.to_visit.put((next_url, depth + 1))
                        # Extract JS files
                        for script in soup.find_all('script', src=True):
                            js_url = urljoin(url, script['src'])
                            if js_url.endswith('.js'):
                                self.js_files.append(js_url)
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {e}")

    def _is_same_domain(self, url):
        """Check if URL is in the same domain."""
        base_domain = urlparse(self.base_url).netloc
        url_domain = urlparse(url).netloc
        return base_domain == url_domain

    def get_results(self):
        return {
            'urls': list(self.found_urls),
            'js_files': self.js_files
        }