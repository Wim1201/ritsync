from modules.google_km import bereken_afstand_google

if __name__ == "__main__":
    adres1 = "Dr. Kuyperstraat 5, Dongen"
    adres2 = "Hoofdstraat 8, 's Gravenmoer"

    afstand = bereken_afstand_google(adres1, adres2)
    print(f"↔️ Afstand tussen '{adres1}' en '{adres2}': {afstand} km")
