import re
from urllib.parse import urlparse, parse_qs
from src.utils import extract_js_endpoints

class Parser:
    @staticmethod
    def parse_js_for_endpoints(js_content):
        """Parse JS content for potential API endpoints."""
        endpoints = extract_js_endpoints(js_content)
        return endpoints

    @staticmethod
    def extract_forms(html_content):
        """Extract forms and their parameters from HTML."""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'lxml')
        forms = []
        for form in soup.find_all('form'):
            action = form.get('action', '')
            method = form.get('method', 'get').lower()
            inputs = []
            for inp in form.find_all('input'):
                name = inp.get('name')
                if name:
                    inputs.append(name)
            forms.append({
                'action': action,
                'method': method,
                'inputs': inputs
            })
        return forms

    @staticmethod
    def extract_urls_from_html(html_content, base_url):
        """Extract all URLs from HTML."""
        from urllib.parse import urljoin
        soup = BeautifulSoup(html_content, 'lxml')
        urls = set()
        for tag in soup.find_all(['a', 'link', 'script', 'img'], href=True):
            url = urljoin(base_url, tag['href'])
            urls.add(url)
        return list(urls)