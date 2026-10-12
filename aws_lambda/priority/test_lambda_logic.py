import unittest
import json
from pathlib import Path

# Import backend and lambda implementations
from backend.app.risk import compute_priority as backend_compute
from aws_lambda.priority.app import compute_priority as lambda_compute

class TestLambdaRiskScoring(unittest.TestCase):
    def test_normal_input(self):
        payload = {"severity": 3, "water_depth_cm": 10, "critical_infra": False}
        self.assertEqual(lambda_compute(payload), backend_compute(payload))

    def test_missing_optional_fields(self):
        # water_depth_cm omitted, defaults to 0; critical_infra omitted, defaults to False
        payload = {"severity": 2}
        expected = backend_compute({"severity": 2, "water_depth_cm": 0, "critical_infra": False})
        self.assertEqual(lambda_compute(payload), expected)

    def test_invalid_severity_type(self):
        payload = {"severity": "high", "water_depth_cm": 5, "critical_infra": False}
        with self.assertRaises(Exception):
            lambda_compute(payload)

    def test_negative_values(self):
        payload = {"severity": -1, "water_depth_cm": -5, "critical_infra": False}
        # The function does not explicitly validate negativity, it just computes
        self.assertEqual(lambda_compute(payload), backend_compute(payload))

    def test_extra_fields_ignored(self):
        payload = {"severity": 4, "water_depth_cm": 8, "critical_infra": True, "extra": "ignore"}
        # Lambda implementation extracts only needed keys, so extra is ignored
        self.assertEqual(lambda_compute(payload), backend_compute(payload))

if __name__ == "__main__":
    unittest.main()
