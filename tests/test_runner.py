import sys
import os

# Zorg dat backend/ in het pad staat
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from backend.services.ritsync_service import bereken_kilometers

print("=== RITTEST ===\n")

# Simuleer input: afsprakenlijst met zakelijke en privé-afspraken
adressen = [
    {
        "adres": "Paleisring 5, Tilburg, Nederland",
        "type": "zakelijk"
    },
    {
        "adres": "Stationsstraat 20, 4811 BB Breda, Nederland",
        "type": "privé"
    },
    {
        "adres": "Nieuwstraat 3, Goirle, Nederland",
        "type": "zakelijk"
    },
    {
        "adres": "Hoofdstraat 77, Oosterhout, Nederland",
        "type": "onbekend"
    }
]

print(f"Aantal invoerafspraken: {len(adressen)}")
print("Invoeradressen:", [a["adres"] for a in adressen])
print()

# Instellingen
thuisadres = "Dr. Kuyperstraat 5, Dongen, Nederland"
kantooradres = "Kantoorstraat 1, Dongen, Nederland"

# Mock afstandsfunctie
def mock_get_distance_km(van, naar):
    routes = {
        ("Dr. Kuyperstraat 5, Dongen, Nederland", "Paleisring 5, Tilburg, Nederland"): 20.0,
        ("Paleisring 5, Tilburg, Nederland", "Nieuwstraat 3, Goirle, Nederland"): 15.0,
        ("Nieuwstraat 3, Goirle, Nederland", "Dr. Kuyperstraat 5, Dongen, Nederland"): 15.0,
        ("Dr. Kuyperstraat 5, Dongen, Nederland", "Kantoorstraat 1, Dongen, Nederland"): 2.0,
        ("Kantoorstraat 1, Dongen, Nederland", "Dr. Kuyperstraat 5, Dongen, Nederland"): 2.0,
    }
    return routes.get((van, naar), 10.0)  # standaard 10 km

# Test uitvoeren
try:
    ketens, afstanden_per_keten, totaal_km, waarschuwingen = bereken_kilometers(
        adressen,
        mock_get_distance_km,
        thuisadres,
        kantooradres
    )

    print("=== RESULTAAT ===\n")
    for i, (keten, afstand) in enumerate(zip(ketens, afstanden_per_keten), 1):
        print(f"Keten {i}:")
        for punt in keten:
            print(f"  - {punt}")
        print(f"  Totale afstand deze keten: {afstand:.2f} km\n")

    print(f"Totale zakelijke kilometers: {totaal_km:.2f} km")

    if waarschuwingen:
        print("\n=== WAARSCHUWINGEN ===")
        for melding in waarschuwingen:
            print(f"⚠️  {melding}")

except Exception as e:
    print("FOUT tijdens uitvoering:", str(e))
