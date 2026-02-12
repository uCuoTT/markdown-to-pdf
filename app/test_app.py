import unittest
from app import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_page_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        self.assertIn(b"Cloud Converter", response.data)

if __name__ == "__main__":
    unittest.main()