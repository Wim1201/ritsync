import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request, flash, send_from_directory
from backend.services.ocr_service import process_txt_file
from backend.services.export_service import exporteer_excel, exporteer_pdf

app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")
app.secret_key = "geheime_sleutel_voor_flash_berichten"
UPLOAD_FOLDER = "backend/uploads"
EXPORT_FOLDER = "data/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

TOEGESTANE_EXTENSIES = {"txt"}

def extensie_toegestaan(bestandsnaam):
    return '.' in bestandsnaam and bestandsnaam.rsplit('.', 1)[1].lower() in TOEGESTANE_EXTENSIES

@app.route("/uploadpagina", methods=["GET"])
def uploadpagina():
    return render_template("upload_form.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "files" not in request.files:
        flash("Geen bestanden ontvangen.")
        return render_template("upload_form.html")

    bestanden = request.files.getlist("files")
    analyse = []

    for bestand in bestanden:
        if bestand.filename == "":
            continue
        if not extensie_toegestaan(bestand.filename):
            flash(f"Bestandstype niet toegestaan: {bestand.filename}")
            continue

        bestandspad = os.path.join(UPLOAD_FOLDER, bestand.filename)
        bestand.save(bestandspad)
        analyse.append(process_txt_file(bestandspad))

    if not analyse:
        flash("Geen geldige bestanden geüpload of geen tekst herkend.")
        return render_template("upload_form.html")

    excel_pad = exporteer_excel(analyse)
    pdf_pad = exporteer_pdf(analyse)

    excel_bestand = os.path.basename(excel_pad)
    pdf_bestand = os.path.basename(pdf_pad)

    return render_template("resultaat.html", resultaten=analyse, excel_bestand=excel_bestand, pdf_bestand=pdf_bestand)

@app.route("/download/<bestand>")
def download(bestand):
    return send_from_directory(EXPORT_FOLDER, bestand, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
