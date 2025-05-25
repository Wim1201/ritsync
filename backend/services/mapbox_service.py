# backend/services/mapbox_service.py
import os
import requests

def bereken_afstand_mapbox(van, naar):
    """
    Roept de Mapbox Directions API aan om de afstand (in km) tussen twee adressen te berekenen.
    Vereist: een geldige MAPBOX_TOKEN in de .env of os.environ.
    """
    api_key = os.getenv("MAPBOX_TOKEN")
    if not api_key:
        raise ValueError("MAPBOX_TOKEN ontbreekt in de omgeving")

    # Geocodeer de adressen naar coördinaten (vereenvoudigde vorm)
    def geocode(adres):
        url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{adres}.json"
        params = {"access_token": api_key}
        resp = requests.get(url, params=params).json()
        if resp.get("features"):
            return resp["features"][0]["center"]  # [lon, lat]
        return None

    coord_van = geocode(van)
    coord_naar = geocode(naar)

    if not coord_van or not coord_naar:
        raise ValueError(f"Geocoding mislukt voor: {van} of {naar}")

    # Bereken routeafstand
    route_url = (
        f"https://api.mapbox.com/directions/v5/mapbox/driving/"
        f"{coord_van[0]},{coord_van[1]};{coord_naar[0]},{coord_naar[1]}"
    )
    route_params = {"access_token": api_key, "overview": "false"}
    r = requests.get(route_url, params=route_params).json()

    if "routes" in r and len(r["routes"]) > 0:
        afstand_meter = r["routes"][0]["distance"]
        return round(afstand_meter / 1000, 1)
    else:
        raise ValueError("Geen route gevonden")
