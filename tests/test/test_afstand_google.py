import os
import requests
from dotenv import load_dotenv

# ✅ .env-bestand laden vanuit project root
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.env'))
load_dotenv(dotenv_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_distance(origin, destination):
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY ontbreekt in .env-bestand")

    endpoint = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    # ⛔️ Foutlog als status niet OK
    if data["status"] != "OK":
        print("🔍 Debug: API response =", data)
        print("📡 URL:", response.url)
        raise Exception(f"API fout: {data['status']}")

    leg = data["routes"][0]["legs"][0]
    return {
        "afstand": leg["distance"]["text"],
        "tijd": leg["duration"]["text"]
    }

if __name__ == "__main__":
    origin = "Amsterdam"
    destination = "Rotterdam"

    try:
        print("🔐 Loaded API KEY prefix:", GOOGLE_API_KEY[:10])
        result = get_distance(origin, destination)
        print(f"🚗 {origin} → {destination}")
        print(f"📏 Afstand: {result['afstand']} | 🕒 Reistijd: {result['tijd']}")
    except Exception as e:
        print(f"❌ Fout bij ophalen afstand: {e}")
