# AIBountyHunter

A Python-based bug bounty tool for automated web vulnerability scanning.

## Features

- Reconnaissance: Crawl websites to discover URLs and JS files.
- Parameter Extraction: Extract parameters from URLs and forms.
- Vulnerability Scanning: Scan for XSS, SQLi, IDOR, SSRF using simple heuristics.
- Async Scanning: Concurrent requests for efficiency.
- Stealth: Random user agents and delays.
- Reporting: Generate reports in HTML, JSON, TXT formats.

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`

## Usage

python main.py <target_url>

## Example

python main.py http://example.com

Reports will be generated in the `reports/` directory.