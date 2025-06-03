# modules/ocr_reader.py

from PIL import Image
import pytesseract
import fitz  # PyMuPDF
import re

def lees_tekst_van_bestand(pad):
    """
    Leest tekst uit PNG, JPG of PDF bestand.
    """
    if pad.lower().endswith(".pdf"):
        return _lees_pdf(pad)
    else:
        return _lees_afbeelding(pad)

def _lees_afbeelding(pad):
    try:
        image = Image.open(pad)
        tekst = pytesseract.image_to_string(image, lang="nld")
        return tekst
    except Exception as e:
        return f"Fout bij afbeelding OCR: {e}"

def _lees_pdf(pad):
    try:
        tekst = ""
        doc = fitz.open(pad)
        for page in doc:
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            tekst += pytesseract.image_to_string(img, lang="nld") + "\n"
        return tekst
    except Exception as e:
        return f"Fout bij PDF OCR: {e}"

def extract_project_info(tekst):
    """
    Extract projectnummer en locatie uit vrije tekst.
    """
    project_match = re.search(r"(project|klant|nr)[^\d]*(\d{3,})", tekst, re.IGNORECASE)
    locatie_match = re.search(r"(adres|locatie)[^\n]*\s*[:\-]?\s*(.+)", tekst, re.IGNORECASE)

    return {
        "project": project_match.group(2) if project_match else None,
        "locatie": locatie_match.group(2).strip() if locatie_match else None
    }
