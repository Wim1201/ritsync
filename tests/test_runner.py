import datetime
import sys
import os

# Zorg dat backend/services in het pad staat
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend', 'services'))

from ritsync_service import bereken_kilometers

print("Script gestart")

# Simuleer input: correcte afsprakenlijst
adressen = [
    {
        "adres": "Paleisring 5, Tilburg, Nederland",
        "tijdstip": datetime.datetime(2025, 5, 30, 9, 0)
    },
    {
        "adres": "Stationsstraat 20, 4811 BB Breda, Nederland",
        "tijdstip": datetime.datetime(2025, 5, 30, 11, 30)
    },
    {
        "adres": "Nieuwstraat 3, Goirle, Nederland",
        "tijdstip": datetime.datetime(2025, 5, 30, 15, 0)
    }
]

print(f"Aantal adressen gevonden: {len(adressen)}")
print("Adressen:", [a["adres"] for a in adressen])

# Testinstellingen
thuisadres = "Dr. Kuyperstraat 5, Dongen, Nederland"
kantooradres = "Kantoorstraat 1, Dongen, Nederland"

# Mock afstandsfunctie
def mock_get_distance_km(van, naar):
    routes = {
        ("Dr. Kuyperstraat 5, Dongen, Nederland", "Paleisring 5, Tilburg, Nederland"): 20.0,
        ("Paleisring 5, Tilburg, Nederland", "Dr. Kuyperstraat 5, Dongen, Nederland"): 20.0,
        ("Kantoorstraat 1, Dongen, Nederland", "Stationsstraat 20, 4811 BB Breda, Nederland"): 25.0,
        ("Stationsstraat 20, 4811 BB Breda, Nederland", "Dr. Kuyperstraat 5, Dongen, Nederland"): 25.0,
        ("Kantoorstraat 1, Dongen, Nederland", "Nieuwstraat 3, Goirle, Nederland"): 15.0,
        ("Nieuwstraat 3, Goirle, Nederland", "Dr. Kuyperstraat 5, Dongen, Nederland"): 15.0,
    }
    return routes.get((van, naar), 10.0)  # standaard 10 km indien route niet gespecificeerd

# Uitvoeren
try:
    ketens, totalen = bereken_kilometers(adressen, mock_get_distance_km, thuisadres, kantooradres)
    print("\nResultaat:")
    for i, (keten, totaal) in enumerate(zip(ketens, totalen), 1):
        print(f"Keten {i}:")
        for punt in keten:
            print(f"  - {punt}")
        print(f"  Totale kilometers: {totaal:.2f} km\n")
except Exception as e:
    print("Fout tijdens berekening:", str(e))
