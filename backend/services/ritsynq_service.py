import re
import pytesseract
from PIL import Image

# Locatie Tesseract (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def ocr_afbeelding(pad):
    try:
        image = Image.open(pad)
        tekst = pytesseract.image_to_string(image, lang="eng")
        return tekst
    except Exception as e:
        raise RuntimeError(f"OCR mislukt: {e}")


def extract_addresses(text):
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
    from backend.services.ritsync_service import process_txt_file as analyse
    return analyse(filepath)
