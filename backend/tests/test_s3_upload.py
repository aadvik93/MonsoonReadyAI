import os
import tempfile
import unittest
from pathlib import Path

# Ensure we use the local settings (LOCAL_DEMO=True by default)
from backend.app.utils import upload_to_s3, generate_presigned_url, settings

class TestS3UploadLocalDemo(unittest.TestCase):
    def setUp(self):
        # Ensure demo mode is on for test isolation
        self.original_demo = settings.LOCAL_DEMO
        settings.LOCAL_DEMO = True
        # Use a temporary file as the upload source
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b"test content")
        self.temp_file.flush()
        self.filename = os.path.basename(self.temp_file.name)

    def tearDown(self):
        # Clean up temporary file and reset demo flag
        os.unlink(self.temp_file.name)
        settings.LOCAL_DEMO = self.original_demo
        # Remove any uploaded file in the uploads dir
        upload_path = Path(settings.LOCAL_UPLOAD_DIR) / self.filename
        if upload_path.exists():
            upload_path.unlink()

    def test_upload_local_fallback(self):
        # When LOCAL_DEMO is True, upload should copy to uploads directory
        key = upload_to_s3(self.temp_file.name, self.filename)
        expected_path = Path(settings.LOCAL_UPLOAD_DIR) / self.filename
        self.assertTrue(expected_path.exists())
        self.assertEqual(key, str(expected_path))

    def test_presigned_url_local_fallback(self):
        # generate_presigned_url should return a file:// URL in demo mode
        key = upload_to_s3(self.temp_file.name, self.filename)
        url = generate_presigned_url(key)
        self.assertTrue(url.startswith("file://"))
        # The URL should point to the absolute path of the uploaded file
        self.assertIn(str(Path(key).absolute()), url)

if __name__ == "__main__":
    unittest.main()
