import pytesseract
from PIL import Image
import os

def verwerk_ocr(bestandspad):
    try:
        # Controle op bestandstype
        if bestandspad.lower().endswith('.pdf'):
            from pdf2image import convert_from_path
            pagina_afbeeldingen = convert_from_path(bestandspad)
            tekst_resultaten = [pytesseract.image_to_string(pagina) for pagina in pagina_afbeeldingen]
            tekst = "\n".join(tekst_resultaten)
        else:
            afbeelding = Image.open(bestandspad)
            tekst = pytesseract.image_to_string(afbeelding)

        # Dummy-parser voor demonstratie (splits per regel en geef dummy-afstanden)
        regels = tekst.strip().split('\n')
        afspraken = []
        for regel in regels:
            regel = regel.strip()
            if regel:
                afspraken.append({'adres': regel, 'type': 'zakelijk', 'afstand': 0.0})

        return [afspraken] if afspraken else []

    except Exception as e:
        print(f"❌ Fout bij OCR-verwerking: {e}")
        return []
