from backend.services.ors_service import bereken_afstand_ors

afstand = bereken_afstand_ors("Dr. Kuyperstraat 5, Dongen", "Paleisring 5, Tilburg")
print(f"Afstand: {afstand} km")
