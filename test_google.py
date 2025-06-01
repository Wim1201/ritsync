from backend.services.google_service import get_distance_km

afstand = get_distance_km("Dr. Kuyperstraat 5, Dongen", "Paleisring 5, Tilburg")
print(f"Afstand via Google: {afstand} km")
