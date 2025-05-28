import unittest
import requests

class TestDownloadEndpoint(unittest.TestCase):
    def test_download_pdf(self):
        data = {
            "locatie": "Teststraat 1, Testdorp",
            "totaal_km": "125.4",
            "co2": "18.2",
            "declarabel": "ja"
        }

        response = requests.post("http://localhost:5000/download_pdf", data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("application/pdf", response.headers.get("Content-Type", ""))

if __name__ == '__main__':
    unittest.main()


