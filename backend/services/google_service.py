import os
import requests

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_distance_km(origin, destination):
    if not GOOGLE_API_KEY:
        return 0.0, 0

    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "key": GOOGLE_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()

        if data["status"] == "OK" and data["rows"][0]["elements"][0]["status"] == "OK":
            distance = data["rows"][0]["elements"][0]["distance"]["value"] / 1000.0
            duration = data["rows"][0]["elements"][0]["duration"]["value"]
            return distance, duration
        else:
            return 0.0, 0
    except Exception:
        return 0.0, 0
