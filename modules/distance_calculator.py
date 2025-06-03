# modules/distance_calculator.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY") or os.getenv("GOOGLE_API_KEY")

def bereken_afstand_en_tijd(rit, bestemming=None):
    vertrek = rit.get("vertrek") or rit.get("locatie")
    aankomst = rit.get("aankomst") or bestemming or vertrek

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": vertrek,
        "destinations": aankomst,
        "key": GOOGLE_API_KEY,
        "language": "nl",
        "mode": "driving"
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        resultaat = data["rows"][0]["elements"][0]
        rit["afstand_km"] = resultaat["distance"]["value"] / 1000
        rit["reistijd_min"] = resultaat["duration"]["value"] / 60
    except (KeyError, IndexError):
        rit["afstand_km"] = 0.0
        rit["reistijd_min"] = 0.0

    return rit
