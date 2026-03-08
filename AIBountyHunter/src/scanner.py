import asyncio
import aiohttp
from config import XSS_PAYLOADS, SQLI_PAYLOADS, SSRF_PAYLOADS, IDOR_VALUES, MAX_CONCURRENT_REQUESTS, TIMEOUT
from src.utils import get_random_user_agent, extract_parameters
from src.heuristics import Heuristics
import logging

logger = logging.getLogger(__name__)

class Scanner:
    def __init__(self, urls, forms):
        self.urls = urls
        self.forms = forms
        self.vulnerabilities = []
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
        self.session = None

    async def scan(self):
        """Perform async scanning for vulnerabilities."""
        async with aiohttp.ClientSession(
            headers={'User-Agent': get_random_user_agent()},
            timeout=aiohttp.ClientTimeout(total=TIMEOUT)
        ) as session:
            self.session = session
            tasks = []
            # Scan URLs for XSS, SQLi, SSRF
            for url in self.urls:
                params = extract_parameters(url)
                if params:
                    tasks.extend(self._create_scan_tasks(url, params))
            # Scan forms
            for form in self.forms:
                tasks.extend(self._create_form_scan_tasks(form))
            # Run all tasks
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, dict):
                    self.vulnerabilities.append(result)

    def _create_scan_tasks(self, url, params):
        tasks = []
        # XSS
        for param in params:
            for payload in Heuristics.generate_payloads(XSS_PAYLOADS, 'xss'):
                task = self._test_vulnerability(url, param, payload, 'xss')
                tasks.append(task)
        # SQLi
        for param in params:
            for payload in Heuristics.generate_payloads(SQLI_PAYLOADS, 'sqli'):
                task = self._test_vulnerability(url, param, payload, 'sqli')
                tasks.append(task)
        # SSRF
        for param in params:
            for payload in Heuristics.generate_payloads(SSRF_PAYLOADS, 'ssrf'):
                task = self._test_vulnerability(url, param, payload, 'ssrf')
                tasks.append(task)
        # IDOR
        for param in params:
            for value in IDOR_VALUES:
                task = self._test_idor(url, param, value)
                tasks.append(task)
        return tasks

    def _create_form_scan_tasks(self, form):
        tasks = []
        for input_name in form['inputs']:
            # Similar to URL params
            for payload in Heuristics.generate_payloads(XSS_PAYLOADS, 'xss'):
                task = self._test_form_vulnerability(form, input_name, payload, 'xss')
                tasks.append(task)
        return tasks

    async def _test_vulnerability(self, url, param, payload, vuln_type):
        async with self.semaphore:
            try:
                # Build test URL
                test_url = self._inject_payload(url, param, payload)
                async with self.session.get(test_url) as response:
                    content = await response.text()
                    if Heuristics.classify_vulnerability(response, payload, vuln_type):
                        return {
                            'type': vuln_type,
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'response_code': response.status,
                            'evidence': content[:200]  # snippet
                        }
            except Exception as e:
                logger.error(f"Error testing {url}: {e}")

    async def _test_form_vulnerability(self, form, input_name, payload, vuln_type):
        async with self.semaphore:
            try:
                data = {inp: payload if inp == input_name else 'test' for inp in form['inputs']}
                async with self.session.post(form['action'], data=data) as response:
                    content = await response.text()
                    if Heuristics.classify_vulnerability(response, payload, vuln_type):
                        return {
                            'type': vuln_type,
                            'url': form['action'],
                            'param': input_name,
                            'payload': payload,
                            'response_code': response.status,
                            'evidence': content[:200]
                        }
            except Exception as e:
                logger.error(f"Error testing form {form['action']}: {e}")

    async def _test_idor(self, url, param, value):
        async with self.semaphore:
            try:
                test_url = self._inject_payload(url, param, str(value))
                async with self.session.get(test_url) as response:
                    content = await response.text()
                    if Heuristics.classify_vulnerability(response, str(value), 'idor'):
                        return {
                            'type': 'idor',
                            'url': test_url,
                            'param': param,
                            'payload': str(value),
                            'response_code': response.status,
                            'evidence': content[:200]
                        }
            except Exception as e:
                logger.error(f"Error testing IDOR {url}: {e}")

    def _inject_payload(self, url, param, payload):
        """Inject payload into URL parameter."""
        from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        query[param] = [payload]
        new_query = urlencode(query, doseq=True)
        new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
        return new_url

    def get_vulnerabilities(self):
        return self.vulnerabilities