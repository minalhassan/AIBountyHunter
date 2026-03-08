from src.utils import generate_mutations, is_vulnerable_response

class Heuristics:
    """Simple heuristics for payload generation and vulnerability detection."""

    @staticmethod
    def generate_payloads(base_payloads, vuln_type):
        """Generate mutated payloads for a vulnerability type."""
        all_payloads = []
        for payload in base_payloads:
            all_payloads.extend(generate_mutations(payload))
        return all_payloads

    @staticmethod
    def classify_vulnerability(response, payload, vuln_type):
        """Classify if a response indicates a vulnerability."""
        if vuln_type == 'xss':
            # Check reflection and no sanitization
            return is_vulnerable_response(response.text, payload)
        elif vuln_type == 'sqli':
            # Check for SQL errors or unexpected behavior
            return is_vulnerable_response(response.text, payload) or response.status_code == 500
        elif vuln_type == 'idor':
            # Check if access to unauthorized resource
            # Simple: if response differs significantly
            return len(response.text) > 100  # Placeholder
        elif vuln_type == 'ssrf':
            # Check if internal service responded
            return 'internal' in response.text.lower() or response.status_code == 200
        return False