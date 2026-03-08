import random
import urllib.parse
import re
from config import USER_AGENTS

def get_random_user_agent():
    """Return a random user agent for stealth."""
    return random.choice(USER_AGENTS)

def url_encode(payload):
    """URL encode a payload."""
    return urllib.parse.quote(payload)

def case_mutate(payload):
    """Randomly change case of characters in payload."""
    return ''.join(random.choice([c.upper(), c.lower()]) if c.isalpha() else c for c in payload)

def generate_mutations(payload):
    """Generate simple mutations of a payload: encoding, case changes."""
    mutations = [payload]
    mutations.append(url_encode(payload))
    mutations.append(case_mutate(payload))
    mutations.append(url_encode(case_mutate(payload)))
    return mutations

def extract_parameters(url):
    """Extract query parameters from URL."""
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    return list(params.keys())

def is_vulnerable_response(response_text, payload):
    """Simple heuristic to check if response indicates vulnerability."""
    # For XSS: check if payload is reflected
    if payload in response_text:
        return True
    # For SQLi: check for error messages
    sql_errors = ['sql syntax', 'mysql error', 'sqlite error']
    if any(error in response_text.lower() for error in sql_errors):
        return True
    return False

def extract_js_endpoints(js_content):
    """Extract potential endpoints from JS code."""
    # Simple regex for URLs in JS
    url_pattern = r'https?://[^\s\'"]+'
    urls = re.findall(url_pattern, js_content)
    return urls