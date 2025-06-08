# backend/services/rit_sync_service.py

import os
from dotenv import load_dotenv
from backend.services.google_service import get_route_distance
from datetime import datetime
from operator import itemgetter

load_dotenv()

THUISADRES = os.getenv("THUISADRES")
KANTOORADRES = os.getenv("KANTOORADRES")

def genereer_rittenlijst(agenda_items):
    """
    Genereert een lijst ritten op basis van gesorteerde afspraken en vaste woon-werk routes.
    Verwacht input: lijst dicts met keys: datum (YYYY-MM-DD), starttijd (HH:MM), eindtijd (HH:MM), locatie, omschrijving
    """

    ritten = []
    totaal_km = 0.0
    totaal_woonwerk = 0.0

    # Groepeer afspraken per dag
    afspraken_per_dag = {}
    for item in agenda_items:
        datum = item["datum"]
        afspraken_per_dag.setdefault(datum, []).append(item)

    for datum, afspraken in afspraken_per_dag.items():
        afspraken.sort(key=itemgetter("starttijd"))  # sorteer op tijd

        dag_ritten = []
        laatste_adres = THUISADRES

        # 🚗 Thuis -> Kantoor (woon-werk)
        if afspraken:
            rit1 = maak_rit(datum, THUISADRES, KANTOORADRES, "Woon-werk: Thuis → Kantoor")
            dag_ritten.append(rit1)
            totaal_km += rit1["afstand_km"]
            totaal_woonwerk += rit1["afstand_km"]
            laatste_adres = KANTOORADRES

        # 📍 Kantoor → afspraak → (evt. meer)
        for afspraak in afspraken:
            bestemming = afspraak["locatie"]
            omschrijving = afspraak.get("omschrijving") or afspraak.get("titel") or "Afspraak"

            rit = maak_rit(datum, laatste_adres, bestemming, omschrijving)
            dag_ritten.append(rit)
            totaal_km += rit["afstand_km"]
            laatste_adres = bestemming

        # 🔁 Laatste afspraak → Kantoor
        if afspraken:
            rit2 = maak_rit(datum, laatste_adres, KANTOORADRES, "Terug naar kantoor")
            dag_ritten.append(rit2)
            totaal_km += rit2["afstand_km"]
            laatste_adres = KANTOORADRES

            # Kantoor → Thuis (woon-werk)
            rit3 = maak_rit(datum, KANTOORADRES, THUISADRES, "Woon-werk: Kantoor → Thuis")
            dag_ritten.append(rit3)
            totaal_km += rit3["afstand_km"]
            totaal_woonwerk += rit3["afstand_km"]

        ritten.extend(dag_ritten)

    return {
        "ritten": ritten,
        "totaal_km": round(totaal_km, 1),
        "woonwerk_km": round(totaal_woonwerk, 1),
    }


def maak_rit(datum, vertrek, bestemming, doel):
    """Helperfunctie voor aanmaken rit + afstand ophalen via Google"""
    try:
        route = get_route_distance(vertrek, bestemming)
        return {
            "datum": datum,
            "vertrek": vertrek,
            "bestemming": bestemming,
            "afstand_km": round(route["distance_meters"] / 1000, 1),
            "reistijd": route["duration_text"],
            "doel": doel
        }
    except Exception as e:
        return {
            "datum": datum,
            "vertrek": vertrek,
            "bestemming": bestemming,
            "afstand_km": 0.0,
            "reistijd": "-",
            "doel": f"{doel} (FOUT: {str(e)})"
        }
