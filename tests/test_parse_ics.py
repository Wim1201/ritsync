# tests/test_parse_ics.py

import unittest
from modules.ics_parser import parse_ics
import tempfile

class TestICSParser(unittest.TestCase):
    def setUp(self):
        self.ics_content = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTART;TZID=Europe/Amsterdam:20250601T080000
DTEND;TZID=Europe/Amsterdam:20250601T090000
SUMMARY:Bezoek klant 101
LOCATION:Dr. Kuyperstraat 5, Dongen
END:VEVENT
BEGIN:VEVENT
DTSTART;TZID=Europe/Amsterdam:20250602T140000
DTEND;TZID=Europe/Amsterdam:20250602T150000
SUMMARY:Opvolging project 202
LOCATION:Hoofdstraat 12, Tilburg
END:VEVENT
END:VCALENDAR"""

    def test_parse_ics(self):
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write(self.ics_content)
            tmp.seek(0)
            result = parse_ics(tmp.name)

        expected = [
            {
                "datum": "2025-06-01",
                "tijd": "08:00",
                "locatie": "Dr. Kuyperstraat 5, Dongen",
                "project": "101"
            },
            {
                "datum": "2025-06-02",
                "tijd": "14:00",
                "locatie": "Hoofdstraat 12, Tilburg",
                "project": "202"
            }
        ]

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
