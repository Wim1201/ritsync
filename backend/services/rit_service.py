# backend/services/rit_service.py
import re
from backend.services.google_service import bereken_afstanden_google

def detecteer_adressen(tekst):
    """
    Herkent adressen of locatie-regels op basis van simpele patronen.
    Voor nu zoeken we naar regels met postcode-formaat (1234 AB) of straatnamen.
    """
    regels = tekst.splitlines()
    adressen = []
    for regel in regels:
        if re.search(r'\d{4}\s?[A-Z]{2}', regel) or "straat" in regel.lower() or "laan" in regel.lower():
            adressen.append(regel.strip())
    return adressen

def bereken_kilometers(adressen, startpunt="Dr. Kuyperstraat 5, Dongen"):
    """
    Bereken retourafstanden tussen startpunt en elk adres via Google Maps API.
    """
    totaal_km = 0
    ritten = []

    print(f"Startpunt: {startpunt}")
    for adres in adressen:
        print(f"Verwerk adres: {adres}")
        try:
            afstand = bereken_afstand_google(startpunt, adres)
            print(f"Afstand: {afstand:.2f} km")
        except Exception as e:
            print(f"Fout bij {adres}: {e}")
            afstand = 0

        ritten.append({
            "datum": "n.t.b.",
            "van": startpunt,
            "naar": adres,
            "afstand": afstand
        })
        totaal_km += afstand * 2  # retourrit

    return ritten, totaal_km
