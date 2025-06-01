import os
from flask import Blueprint, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename
from backend.services.ocr_service import verwerk_ocr
from backend.services.export_service import exporteer_excel, exporteer_pdf

ocr_bp = Blueprint("ocr", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@ocr_bp.route("/ocr-uploadpagina")
def ocr_uploadpagina():
    return render_template("ocr_upload_form.html")

@ocr_bp.route("/ocr-upload", methods=["POST"])
def ocr_upload():
    if "bestand" not in request.files:
        return "Geen bestand meegegeven", 400

    bestand = request.files["bestand"]

    if bestand.filename == "":
        return "Geen bestand gekozen", 400

    bestandsnaam = secure_filename(bestand.filename)
    opslagpad = os.path.join(UPLOAD_FOLDER, bestandsnaam)
    bestand.save(opslagpad)

    # Verwerk OCR
    resultaten = verwerk_ocr(opslagpad)

    if not resultaten:
        return "Geen resultaten gevonden", 204

    # Exporteer naar Excel en PDF
    excel_pad = exporteer_excel(resultaten)
    pdf_pad = exporteer_pdf(resultaten)

    # Geef PDF terug als download
    return send_file(pdf_pad, as_attachment=True)
