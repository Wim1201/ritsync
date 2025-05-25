import os
import requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def bereken_afstanden_google(startadres, adressen):
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY ontbreekt in .env")

    resultaten = []
    totaal_km = 0.0

    for adres in adressen:
        try:
            response = requests.get(
                "https://maps.googleapis.com/maps/api/distancematrix/json",
                params={
                    "origins": startadres,
                    "destinations": adres,
                    "key": GOOGLE_API_KEY,
                    "language": "nl",
                    "units": "metric"
                }
            )
            data = response.json()
            if data['status'] == 'OK' and data['rows'][0]['elements'][0]['status'] == 'OK':
                afstand_m = data['rows'][0]['elements'][0]['distance']['value']
                afstand_km = afstand_m / 1000
                totaal_km += afstand_km * 2  # Retour

                resultaten.append({
                    "van": startadres,
                    "naar": adres,
                    "afstand": afstand_km
                })
            else:
                print(f"Geen resultaat voor {adres}: {data}")
        except Exception as e:
            print(f"Fout bij ophalen afstand voor {adres}: {e}")

    return resultaten, totaal_km

