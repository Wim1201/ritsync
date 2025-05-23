# backend/services/rit_service.py
import re

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
    Simuleert afstanden tussen het startpunt en adressen (of tussen adressen onderling).
    Voor nu gebruiken we vaste voorbeeldafstanden.
    """
    afstand_per_adres = {
        "Rijen": 11,
        "Tilburg": 20,
        "Goirle": 25,
        "Breda": 28,
        "Haarlem": 130,
        "Oud-Heusden": 38,
        "Waalwijk": 30
    }

    totaal_km = 0
    resultaten = []

    vorige = startpunt
    for adres in adressen:
        afstand = next((afstand_per_adres[plaats] for plaats in afstand_per_adres if plaats.lower() in adres.lower()), 5)
        resultaten.append((vorige, adres, afstand))
        totaal_km += afstand
        vorige = adres

    # Terug naar Dongen
    resultaten.append((vorige, startpunt, 15))
    totaal_km += 15

    return resultaten, totaal_km
