import sys
import os

# 📌 Voeg de projectroot toe aan sys.path zodat backend modules gevonden worden
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.services.ritsync_service import genereer_rittenlijst  # ✅ correcte bestandsnaam

agenda_items = [
    {
        "datum": "2025-06-08",
        "starttijd": "09:00",
        "eindtijd": "10:30",
        "locatie": "Lange Dreef 20, Breda",
        "omschrijving": "Klantoverleg Project #123"
    },
    {
        "datum": "2025-06-08",
        "starttijd": "14:00",
        "eindtijd": "15:00",
        "locatie": "Parallelweg 12, Tilburg",
        "omschrijving": "Technisch overleg"
    }
]

resultaat = genereer_rittenlijst(agenda_items)

for rit in resultaat["ritten"]:
    print(f"📅 {rit['datum']}: {rit['vertrek']} → {rit['bestemming']} ({rit['doel']})")
    print(f"  📏 {rit['afstand_km']} km | ⏱️ {rit['reistijd']}")

print(f"\n🔢 Totale kilometers: {resultaat['totaal_km']} km")
print(f"🏠 Woon-werk kilometers: {resultaat['woonwerk_km']} km")
