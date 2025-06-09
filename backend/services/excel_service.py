import csv
import os
from datetime import datetime

def genereer_excel(ritten):
    bestandsnaam = f"export/ritten_agenda_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    with open(bestandsnaam, mode='w', newline='', encoding='utf-8') as bestand:
        writer = csv.writer(bestand)
        writer.writerow(["Datum", "Tijd", "Van", "Naar", "Omschrijving", "Afstand (km)", "Duur"])
        for rit in ritten:
            writer.writerow([
                rit.get("datum", ""),
                rit.get("tijd", ""),
                rit.get("van", ""),
                rit.get("naar", ""),
                rit.get("omschrijving", ""),
                rit.get("afstand", ""),
                rit.get("duur", "")
            ])
    return bestandsnaam

