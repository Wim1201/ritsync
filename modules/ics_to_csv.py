# modules/ics_to_csv.py

import csv
import os
from modules.ics_parser import parse_ics

def ics_to_csv(ics_path, csv_path="exports/ritten_van_agenda.csv"):
    """
    Converteert een .ics bestand naar CSV-ritformaat.
    """

    ritten = parse_ics(ics_path)

    # Zorg dat de exportmap bestaat
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["datum", "tijd", "locatie", "project"])
        writer.writeheader()
        for rit in ritten:
            writer.writerow(rit)

    return csv_path
