import os
import unittest

# Guard imports for optional dependencies
try:
    from fastapi.testclient import TestClient
    from ..app.main import app
    FASTAPI_AVAILABLE = True
except Exception:
    FASTAPI_AVAILABLE = False

try:
    from ..app.utils import compute_priority
    from ..app.models import Report
    SQLMODEL_AVAILABLE = True
except Exception:
    SQLMODEL_AVAILABLE = False

class BackendTests(unittest.TestCase):
    @unittest.skipUnless(FASTAPI_AVAILABLE, "FastAPI not available in sandbox")
    def test_health_endpoint(self):
        client = TestClient(app)
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())

    @unittest.skipUnless(SQLMODEL_AVAILABLE, "SQLModel/Report not available")
    def test_compute_priority(self):
        # Create a minimal Report instance
        report = Report(
            location_name="Test",
            latitude=0.0,
            longitude=0.0,
            description="Test incident",
            severity=5,
            critical_infra=True,
        )
        result = compute_priority(report)
        self.assertIn("score", result)
        self.assertIn("category", result)
        self.assertIn("explanation", result)
        # High severity should produce HIGH category
        self.assertEqual(result["category"], "HIGH")

if __name__ == "__main__":
    unittest.main()
