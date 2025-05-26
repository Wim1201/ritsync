from dotenv import load_dotenv
load_dotenv()
import os
import requests
from urllib.parse import urlencode

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_distance_km(origin, destination):
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is niet ingesteld in .env bestand")

    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "mode": "driving",
        "language": "nl-NL",
        "key": GOOGLE_API_KEY
    }

    url = f"{base_url}?{urlencode(params)}"
    response = requests.get(url)
    data = response.json()

    try:
        element = data["rows"][0]["elements"][0]
        if element["status"] == "OK":
            meters = element["distance"]["value"]
            return round(meters / 1000, 1)  # kilometer afronden op 1 decimaal
        else:
            print(f"Google Distance Matrix error: {element['status']}")
            return 0
    except (KeyError, IndexError):
        print("Fout bij het verwerken van de Google API-response:", data)
        return 0
