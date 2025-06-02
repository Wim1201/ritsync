# modules/google_km.py

import logging

# Mock fallback functie om afstand te berekenen tussen twee adressen
def bereken_afstand_google(van_adres, naar_adres):
    """
    Berekent afstand tussen twee adressen.
    In de productieversie wordt deze functie vervangen door een Google Maps Distance Matrix API call.
    """
    try:
        # 🔧 Simuleer een afstand op basis van stringlengte (placeholder logica)
        afstand = round(abs(len(van_adres) - len(naar_adres)) + 5.5, 2)
        logging.info(f"Afstand {van_adres} -> {naar_adres} ≈ {afstand} km (mock)")
        return afstand
    except Exception as e:
        logging.error(f"Fout bij afstandberekening: {e}")
        return 0.0
