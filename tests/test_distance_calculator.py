# tests/test_distance_calculator.py

import unittest
from unittest.mock import patch
from modules.distance_calculator import bereken_afstand_en_tijd

class TestDistanceCalculator(unittest.TestCase):

    @patch("modules.distance_calculator.requests.get")
    def test_afstand_en_tijd_berekening(self, mock_get):
        mock_response = {
            "rows": [
                {"elements": [
                    {
                        "distance": {"value": 12345},
                        "duration": {"value": 987}
                    }
                ]}
            ]
        }
        mock_get.return_value.json.return_value = mock_response

        rit = {
            "locatie": "Dr. Kuyperstraat 5, Dongen"
        }

        verrijkt = bereken_afstand_en_tijd(rit, bestemming="Brouwerstraat 9, Breda")

        self.assertEqual(verrijkt["afstand_km"], 12.345)
        self.assertEqual(verrijkt["reistijd_min"], 16.45)

if __name__ == '__main__':
    unittest.main()
