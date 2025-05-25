# backend/services/ocr_service.py
r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import pytesseract
from PIL import Image
import os

def extract_text_from_image(image_path):
    """
    Voert OCR uit op de opgegeven afbeelding en retourneert de gedetecteerde tekst.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Bestand niet gevonden: {image_path}")
    try:
        tekst = pytesseract.image_to_string(Image.open(image_path), lang='nld')
        return tekst
    except Exception as e:
        print(f"Fout bij OCR: {e}")
        return ""

