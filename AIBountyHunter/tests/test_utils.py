import unittest
from src.utils import generate_mutations, is_vulnerable_response

class TestUtils(unittest.TestCase):
    def test_generate_mutations(self):
        payload = "<script>alert(1)</script>"
        mutations = generate_mutations(payload)
        self.assertIn(payload, mutations)
        self.assertTrue(len(mutations) > 1)

    def test_is_vulnerable_response(self):
        response = "Error: SQL syntax"
        self.assertTrue(is_vulnerable_response(response, "test"))

if __name__ == '__main__':
    unittest.main()