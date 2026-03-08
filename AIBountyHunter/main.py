import asyncio
import sys
import logging
from src.crawler import Crawler
from src.parser import Parser
from src.scanner import Scanner
from src.reporter import Reporter

logger = logging.getLogger(__name__)

async def main(target_url):
    """Main function to run the AIBountyHunter."""
    logger.info(f"Starting scan on {target_url}")

    # Step 1: Reconnaissance - Crawl the site
    crawler = Crawler(target_url)
    await crawler.crawl()
    results = crawler.get_results()
    urls = results['urls']
    js_files = results['js_files']

    logger.info(f"Found {len(urls)} URLs and {len(js_files)} JS files")

    # Step 2: Parse JS for endpoints
    js_endpoints = []
    for js_url in js_files:
        # Fetch JS content (simplified, assume we have it)
        # In real, fetch async
        pass  # Placeholder

    # Step 3: Extract forms and parameters
    forms = []
    for url in urls[:10]:  # Limit for demo
        # Fetch HTML (simplified)
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    forms.extend(Parser.extract_forms(html))

    logger.info(f"Found {len(forms)} forms")

    # Step 4: Scan for vulnerabilities
    scanner = Scanner(urls, forms)
    await scanner.scan()
    vulnerabilities = scanner.get_vulnerabilities()

    logger.info(f"Found {len(vulnerabilities)} vulnerabilities")

    # Step 5: Generate reports
    reporter = Reporter(vulnerabilities)
    reporter.generate_reports()

    logger.info("Reports generated")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <target_url>")
        sys.exit(1)
    target_url = sys.argv[1]
    asyncio.run(main(target_url))