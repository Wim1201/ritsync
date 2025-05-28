import re
import pytesseract
from PIL import Image
from backend.services.google_service import get_distance_km

START_ADDRESS = "Dr. Kuyperstraat, Dongen"

# Verwijs naar de juiste locatie van Tesseract op Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def ocr_afbeelding(pad):
    try:
        image = Image.open(pad)
        tekst = pytesseract.image_to_string(image, lang="eng")
        return tekst
    except Exception as e:
        raise RuntimeError(f"OCR mislukt: {e}")

def extract_addresses(text):
    # Regex voor postcode + huisnummer (bv. 1234 AB Stationsstraat 1)
    pattern = r"(\d{4}\s?[A-Z]{2})\s+([\w\s]+\d+)"
    matches = re.findall(pattern, text)
    return ["{} {}".format(p[1], p[0]) for p in matches]

def detect_category(text):
    if "#woonwerk" in text.lower():
        return "woonwerk"
    elif "#privé" in text.lower():
        return "prive"
    else:
        return "zakelijk"

def process_txt_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    addresses = extract_addresses(content)
    category = detect_category(content)

    results = []
    km_total = 0.0
    km_woonwerk = 0.0

    for addr in addresses:
        try:
            km = get_distance_km(START_ADDRESS, addr)
        except Exception as e:
            km = 0.0
        result = {
            "adres": addr,
            "afstand_km": round(km, 2),
            "categorie": category
        }
        results.append(result)
        km_total += km
        if category == "woonwerk":
            km_woonwerk += km

    return {
        "bestand": filepath,
        "inhoud": content,
        "resultaten": results,
        "km_totaal": round(km_total, 2),
        "km_woonwerk": round(km_woonwerk, 2)
    }
