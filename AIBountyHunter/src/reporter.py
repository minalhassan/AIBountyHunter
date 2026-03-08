import json
import os
from jinja2 import Template
from config import REPORT_FORMATS

class Reporter:
    def __init__(self, vulnerabilities, output_dir='reports'):
        self.vulnerabilities = vulnerabilities
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_reports(self):
        """Generate reports in specified formats."""
        for fmt in REPORT_FORMATS:
            if fmt == 'json':
                self._generate_json()
            elif fmt == 'html':
                self._generate_html()
            elif fmt == 'txt':
                self._generate_txt()

    def _generate_json(self):
        """Generate JSON report."""
        with open(os.path.join(self.output_dir, 'report.json'), 'w') as f:
            json.dump(self.vulnerabilities, f, indent=4)

    def _generate_html(self):
        """Generate HTML report."""
        template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>AIBountyHunter Report</title>
            <style>
                body { font-family: Arial, sans-serif; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>Vulnerability Report</h1>
            <table>
                <tr>
                    <th>Type</th>
                    <th>URL</th>
                    <th>Parameter</th>
                    <th>Payload</th>
                    <th>Response Code</th>
                    <th>Evidence</th>
                </tr>
                {% for vuln in vulnerabilities %}
                <tr>
                    <td>{{ vuln.type }}</td>
                    <td>{{ vuln.url }}</td>
                    <td>{{ vuln.param }}</td>
                    <td>{{ vuln.payload }}</td>
                    <td>{{ vuln.response_code }}</td>
                    <td>{{ vuln.evidence }}</td>
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        """)
        html_content = template.render(vulnerabilities=self.vulnerabilities)
        with open(os.path.join(self.output_dir, 'report.html'), 'w') as f:
            f.write(html_content)

    def _generate_txt(self):
        """Generate TXT report."""
        with open(os.path.join(self.output_dir, 'report.txt'), 'w') as f:
            f.write("AIBountyHunter Vulnerability Report\n\n")
            for vuln in self.vulnerabilities:
                f.write(f"Type: {vuln['type']}\n")
                f.write(f"URL: {vuln['url']}\n")
                f.write(f"Parameter: {vuln['param']}\n")
                f.write(f"Payload: {vuln['payload']}\n")
                f.write(f"Response Code: {vuln['response_code']}\n")
                f.write(f"Evidence: {vuln['evidence']}\n\n")