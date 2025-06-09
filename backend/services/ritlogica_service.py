from backend.services.google_service import get_route_distance
import os

THUIS = os.getenv("THUISADRES", "Dr. Kuyperstraat 5, Dongen")
KANTOOR = os.getenv("KANTOORADRES", "Hoge Ham 104, Dongen")

def genereer_rittenlijst(afspraken):
    ritten = []
    totaal_km = 0.0
    woonwerk_km = 0.0

    if not afspraken:
        return {"ritten": [], "totaal_km": 0.0, "woonwerk_km": 0.0}

    afspraken.sort(key=lambda x: (x["datum"], x["starttijd"]))

    locaties = [THUIS, KANTOOR] + [a["locatie"] for a in afspraken] + [KANTOOR, THUIS]

    for i in range(len(locaties) - 1):
        vertrek = locaties[i]
        bestemming = locaties[i + 1]
        afstand, duur = get_route_distance(vertrek, bestemming)

        if vertrek == THUIS or bestemming == THUIS:
            woonwerk_km += afstand

        ritten.append({
            "datum": afspraken[0]["datum"],
            "tijd": afspraken[i-1]["starttijd"] if i-1 < len(afspraken) else "",
            "van": vertrek,
            "naar": bestemming,
            "omschrijving": afspraken[i-2]["omschrijving"] if i-2 < len(afspraken) else "",
            "afstand": afstand,
            "duur": duur
        })

        totaal_km += afstand

    return {
        "ritten": ritten,
        "totaal_km": round(totaal_km, 1),
        "woonwerk_km": round(woonwerk_km, 1)
    }
