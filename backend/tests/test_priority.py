import unittest
from types import SimpleNamespace

from backend.app.risk import compute_priority

class TestComputePriority(unittest.TestCase):
    def test_low_severity(self):
        report = SimpleNamespace(severity=1, water_depth_cm=0, critical_infra=False)
        result = compute_priority(report)
        self.assertEqual(result["category"], "LOW")
        self.assertTrue(result["score"] < 8)

    def test_medium_severity(self):
        report = SimpleNamespace(severity=3, water_depth_cm=20, critical_infra=False)
        result = compute_priority(report)
        self.assertEqual(result["category"], "MEDIUM")
        self.assertTrue(8 <= result["score"] < 15)

    def test_high_severity(self):
        report = SimpleNamespace(severity=5, water_depth_cm=100, critical_infra=True)
        result = compute_priority(report)
        self.assertEqual(result["category"], "HIGH")
        self.assertTrue(result["score"] >= 15)

if __name__ == "__main__":
    unittest.main()
