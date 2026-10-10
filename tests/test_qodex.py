import unittest
import re
from qodex.scanner import SECRET_PATTERNS

class TestQodex(unittest.TestCase):
    def test_secret_patterns(self):
        sample_diff = 'export GITHUB_TOKEN="ghp_123456789012345678901234567890123456"'
        matched = False
        for pattern, desc in SECRET_PATTERNS:
            if re.findall(pattern, sample_diff):
                matched = True
                self.assertEqual(desc, "GitHub Personal Access Token")
                break
        self.assertTrue(matched)

    def test_clean_diff_passes(self):
        clean_diff = 'def hello():\n    return "world"'
        for pattern, _ in SECRET_PATTERNS:
            self.assertEqual(len(re.findall(pattern, clean_diff)), 0)

if __name__ == "__main__":
    unittest.main()
