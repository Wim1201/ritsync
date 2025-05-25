# backend/services/ors_service.py
import os
import requests

ORS_API_KEY = os.getenv("ORS_API_KEY")

GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def geocode_adres(adres):
    params = {
        "api_key": ORS_API_KEY,
        "text": adres,
        "size": 1
    }
    response = requests.get(GEOCODE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    features = data.get("features")
    if not features:
        raise ValueError(f"Adres '{adres}' niet gevonden")

    coords = features[0]["geometry"]["coordinates"]  # [lon, lat]
    return coords[1], coords[0]  # (lat, lon)


def bereken_afstand_ors(adres_van, adres_naar):
    lat1, lon1 = geocode_adres(adres_van)
    lat2, lon2 = geocode_adres(adres_naar)

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "coordinates": [[lon1, lat1], [lon2, lat2]]
    }

    response = requests.post(DIRECTIONS_URL, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    afstand_meter = data["features"][0]["properties"]["segments"][0]["distance"]
    afstand_km = round(afstand_meter / 1000, 1)
    return afstand_km
