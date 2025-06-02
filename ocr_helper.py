from PIL import Image
import pytesseract

def lees_tekst_van_afbeelding(pad_naar_afbeelding):
    tekst = pytesseract.image_to_string(Image.open(pad_naar_afbeelding), lang='nld')
    return tekst
