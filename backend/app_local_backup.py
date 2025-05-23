from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Geen bestand meegegeven", 400
    file = request.files['file']
    if file.filename == '':
        return "Geen geselecteerd bestand", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    text = pytesseract.image_to_string(Image.open(filepath))
    result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ocr_result.txt')
    with open(result_path, 'w', encoding='utf-8') as f:
        f.write(text)

    return f"<h2>OCR-resultaat:</h2><pre>{text}</pre><a href='/'>Terug</a>"

if __name__ == '__main__':
    app.run(debug=True)
from flask import send_file
from fpdf import FPDF

@app.route('/download')
def download_pdf():
    text_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ocr_result.txt')
    
    if not os.path.exists(text_path):
        return "Geen OCR-resultaat beschikbaar om te downloaden.", 404

    with open(text_path, 'r', encoding='utf-8') as file:
        content = file.read()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Voeg tekst toe, regel voor regel
    for line in content.splitlines():
        pdf.cell(200, 10, txt=line, ln=True)

    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ocr_result.pdf')
    pdf.output(output_path)

    return send_file(output_path, as_attachment=True)
