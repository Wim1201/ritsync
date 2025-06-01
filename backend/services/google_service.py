import os
import requests
from dotenv import load_dotenv

# Laad .env als dit lokaal nog niet automatisch gebeurt
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_distance_km(origin, destination):
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY ontbreekt in .env-bestand")

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
            meters = data["rows"][0]["elements"][0]["distance"]["value"]
            kilometers = round(meters / 1000.0, 1)  # nauwkeurigheid op 100 meter
            return kilometers
        else:
            print(f"Foutmelding van Google API: {data}")
            return 0.0
    except Exception as e:
        print(f"API-fout: {e}")
        return 0.0
