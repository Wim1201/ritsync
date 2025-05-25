# test_google_service.py
from backend.services.rit_service import bereken_kilometers

print("Script gestart")

adressen = [
    "Paleisring 5, Tilburg, Nederland",
    "Stationsstraat 20, 4811 BB Breda, Nederland",
    "Nieuwstraat 3, Goirle, Nederland"
]

print(f"Aantal adressen gevonden: {len(adressen)}")
print("Adressen:", adressen)

try:
    ritten, totaal = bereken_kilometers(adressen)
    print("Resultaten ontvangen")

    print("\nOverzicht van ritten:")
    for rit in ritten:
        print(f"- Van {rit['van']} naar {rit['naar']}: {rit['afstand']:.2f} km")

    print(f"\nTotaal aantal kilometers (retour): {totaal:.2f} km")

except Exception as e:
    print(f"Fout tijdens berekening: {e}")
