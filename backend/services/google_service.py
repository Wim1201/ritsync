import requests

def get_distance_km(origin, destination):
    # Simuleer afstand voor test (vervang dit indien Google API actief is)
    if not origin or not destination:
        raise ValueError("Oorsprong en bestemming moeten zijn opgegeven.")
    
    print(f"Afstand berekenen van {origin} naar {destination}")
    # Tijdelijk simuleren met vaste waarde
    return 12.5

