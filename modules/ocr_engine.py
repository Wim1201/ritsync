import pytesseract
from PIL import Image

def lees_tekst_van_afbeelding(pad):
    try:
        afbeelding = Image.open(pad)
        tekst = pytesseract.image_to_string(afbeelding, lang='nld')
        return tekst.strip()
    except Exception as e:
        return f"Fout bij OCR: {e}"
