# backend/services/ocr_service.py
from PIL import Image
import pytesseract
import re


def ocr_naar_json(pad_naar_afbeelding):
    """
    Leest een afbeelding en probeert adresregels te extraheren.
    Output: dict in basisstructuur voor PDF.
    """
    try:
        tekst = pytesseract.image_to_string(Image.open(pad_naar_afbeelding))
    except Exception as e:
        return {"fout": f"OCR mislukt: {str(e)}"}

    regels = tekst.splitlines()
    ritten = []
    totaal_km = 0

    for regel in regels:
        if re.search(r'\d{4}\s?[A-Z]{2}', regel):  # Postcodeherkenning
            ritten.append({
                "datum": "n.t.b.",
                "van": "Dongen",
                "naar": regel.strip(),
                "afstand": 15  # voorlopig vaste afstand
            })
            totaal_km += 30  # retour

    return {
        "periode": "voorbeeldweek",
        "totaal_km": totaal_km,
        "verbruik_liter": round(totaal_km / 10, 1),
        "vergoeding": round(totaal_km * 0.23, 2),
        "ritten": ritten
    }
