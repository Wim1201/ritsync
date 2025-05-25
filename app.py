# app.py (plaats in hoofdmap "ritsync")
from flask import Flask, render_template, request
from backend.routes.routes_pdf import pdf_bp
from backend.services.ocr_service import extract_text_from_image
from backend.services.rit_service import detecteer_adressen
import os

app = Flask(__name__, template_folder="frontend/templates")
app.register_blueprint(pdf_bp)

# Correct gescheiden
UPLOAD_FOLDER = os.path.join("backend", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file:
        return "Geen bestand ontvangen", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # OCR uitvoeren
    tekst = extract_text_from_image(filepath)
    adressen = detecteer_adressen(tekst)

    return render_template(
        "result.html",
        adressen=adressen,
        vertrek="Dr. Kuyperstraat 5, Dongen"
    )

if __name__ == "__main__":
    print("=== Start RitSync app ===")
    app.run(debug=True)
