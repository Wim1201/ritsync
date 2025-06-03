# tests/test_ics_to_csv.py

import unittest
import tempfile
import os
from modules.ics_to_csv import ics_to_csv

class TestIcsToCsv(unittest.TestCase):
    def setUp(self):
        self.ics_content = """BEGIN:VCALENDAR
BEGIN:VEVENT
DTSTART;TZID=Europe/Amsterdam:20250601T080000
DTEND;TZID=Europe/Amsterdam:20250601T090000
SUMMARY:Klantbezoek 101
LOCATION:Dr. Kuyperstraat 5, Dongen
END:VEVENT
END:VCALENDAR"""

    def test_csv_output(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".ics") as tmp:
            tmp.write(self.ics_content)
            tmp.seek(0)
            ics_path = tmp.name

        export_path = "exports/test_export.csv"
        result_csv = ics_to_csv(ics_path, csv_path=export_path)

        self.assertTrue(os.path.exists(result_csv))

        with open(result_csv, encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Dr. Kuyperstraat 5", content)
            self.assertIn("101", content)

        os.remove(result_csv)

if __name__ == '__main__':
    unittest.main()
