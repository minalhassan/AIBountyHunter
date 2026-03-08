# AIBountyHunter

An advanced command-line security tool that automatically performs reconnaissance, crawls websites, analyzes endpoints, and tests for vulnerabilities using AI-assisted payload generation and intelligent scanning.

## Features

- **Smart Reconnaissance**: Subdomain discovery, DNS enumeration, WHOIS lookup, technology detection, IP discovery, API endpoint discovery, JavaScript file collection.
- **AI Web Crawling**: Recursive crawling, extract internal links, identify forms and parameters, detect API endpoints, hidden endpoints in JavaScript, avoid external domains.
- **JavaScript Intelligence Engine**: Parse JS files to extract hidden endpoints, API routes, internal URLs, sensitive paths.
- **Parameter Discovery Engine**: Extract parameters from URLs, forms, APIs.
- **AI Vulnerability Analysis Engine**: Analyze HTTP responses for possible vulnerabilities based on reflections, errors, differences, etc.
- **Vulnerability Scanning Modules**: Test for XSS (reflected, DOM, stored), SQL Injection (error-based, boolean-based, time-based), IDOR, Open Redirect, SSRF, Directory Traversal, File Upload, Security Headers.
- **Intelligent Payload Generator**: Dynamically generate payloads with mutations (encoding, case, bypass).
- **Attack Surface Mapping**: Graph representation of the application.
- **Screenshot Engine**: Capture screenshots using Playwright.
- **Stealth Scanning**: Random user agents, delays, retries, proxies.
- **Multithreading/Async Scanning**: Use aiohttp, asyncio, threading.
- **Reporting System**: Professional reports in HTML, JSON, Markdown, PDF.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/minalhassan/AIBountyHunter
   cd AIBountyHunter
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```
   playwright install
   ```

### Linux-Specific Setup

On Linux, ensure Python 3.11+ is installed. Use `python3` and `pip3`:

```
sudo apt update && sudo apt install python3 python3-pip  # Ubuntu/Debian
pip3 install -r requirements.txt
playwright install-deps  # Install system dependencies for Playwright
playwright install
```

For virtual environment:
```
python3 -m venv aibounty_env
source aibounty_env/bin/activate
pip install -r requirements.txt
```

Running:
```
python3 main.py -u https://target.com
```

## Usage

Basic scan:
```
python main.py scan https://target.com
```

Advanced mode:
```
python main.py scan https://target.com --depth 3 --threads 20 --ai --output report.html
```

CLI options:
- `-u / --url`: Target URL
- `--depth`: Crawling depth (default 2)
- `--threads`: Number of threads (default 10)
- `--ai-mode`: Enable AI features
- `--stealth`: Enable stealth mode
- `--output-format`: Output format (html/json/md/pdf, default html)

## Project Structure

```
AIBountyHunter/
├── core/
│   ├── crawler.py
│   ├── request_engine.py
│   ├── ai_engine.py
├── recon/
│   ├── subdomain_enum.py
│   ├── js_parser.py
├── scanners/
│   ├── xss_scanner.py
│   ├── sqli_scanner.py
│   ├── idor_scanner.py
│   ├── ssrf_scanner.py
├── ai/
│   ├── payload_generator.py
│   ├── vulnerability_classifier.py
├── reporting/
│   ├── report_generator.py
├── payloads/
│   ├── xss.txt
│   ├── sqli.txt
├── utils/
│   ├── logger.py
│   ├── config_loader.py
└── main.py
```

## Example Vulnerability Scan Report

See `example_report.html` for a sample output.

## Disclaimer

This tool is for educational and authorized security testing purposes only. Use at your own risk. The author is not responsible for any misuse or damage caused by this tool.

## Contributing

Contributions are welcome! Please open issues or pull requests.

## License

MIT License


