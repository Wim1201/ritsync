import os
import sys
import unittest

# Voeg het pad naar de hoofdmap toe zodat imports goed gaan
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ritsync_service import bereken_kilometers
from google_service import get_distance_km

def main():
    print("Script gestart")

    adressen = [
        "Paleisring 5, Tilburg, Nederland",
        "Stationsstraat 20, 4811 BB Breda, Nederland",
        "Nieuwstraat 3, Goirle, Nederland"
    ]

    print(f"Aantal adressen gevonden: {len(adressen)}")
    print(f"Adressen: {adressen}")

    try:
        totaal_km, woonwerk_km, rittenoverzicht = bereken_kilometers(
            adressen=adressen,
            afstandsfunctie=get_distance_km,
            thuisadres="Dr. Kuyperstraat 5, Dongen, Nederland",
            kantooradres="Tilburg University, Tilburg, Nederland"
        )

        print(f"Totaal aantal kilometers: {totaal_km:.2f} km")
        print(f"Woon-werk kilometers: {woonwerk_km:.2f} km")
        print("Rittenoverzicht:")
        for rit in rittenoverzicht:
            print(rit)

    except Exception as e:
        print(f"Fout tijdens berekening: {e}")

if __name__ == "__main__":
    main()
