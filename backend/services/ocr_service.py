import pytesseract
from PIL import Image
import pdf2image
import os
import json

OUTPUT_FILE = 'ritsync/data/output/ocr_text.json'

def extract_text_from_file(filepath):
    file_ext = os.path.splitext(filepath)[1].lower()

    if file_ext in ['.png', '.jpg', '.jpeg']:
        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)

    elif file_ext == '.pdf':
        images = pdf2image.convert_from_path(filepath)
        text = ''
        for page in images:
            text += pytesseract.image_to_string(page)

    else:
        raise ValueError("Ongeldig bestandstype voor OCR-verwerking.")

    save_text_to_json(text)

def save_text_to_json(text):
    output_path = os.path.abspath(OUTPUT_FILE)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"ocr_text": text}, f, indent=2, ensure_ascii=False)
