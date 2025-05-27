from flask import Flask, render_template, request, flash, send_from_directory
import os
from backend.services.ocr_service import ocr_afbeelding, process_txt_file
from backend.services.export_service import exporteer_excel, exporteer_pdf

app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")
app.secret_key = "geheime_sleutel"

UPLOAD_FOLDER = "backend/uploads"
EXPORT_FOLDER = "data/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

TOEGESTANE_EXTENSIES = {"png", "jpg", "jpeg", "pdf"}

def extensie_toegestaan(bestandsnaam):
    return '.' in bestandsnaam and bestandsnaam.rsplit('.', 1)[1].lower() in TOEGESTANE_EXTENSIES

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ocr-uploadpagina", methods=["GET"])
def ocr_uploadpagina():
    return render_template("ocr_upload_form.html")

@app.route("/ocr-upload", methods=["POST"])
def ocr_upload():
    if "files" not in request.files:
        flash("Geen bestanden ontvangen.")
        return render_template("ocr_upload_form.html")

    bestanden = request.files.getlist("files")
    analyse_resultaten = []

    for bestand in bestanden:
        if bestand.filename == "":
            continue
        if not extensie_toegestaan(bestand.filename):
            flash(f"Bestandstype niet toegestaan: {bestand.filename}")
            continue

        bestandspad = os.path.join(UPLOAD_FOLDER, bestand.filename)
        bestand.save(bestandspad)

        try:
            tekst = ocr_afbeelding(bestandspad)
            txt_path = bestandspad + ".txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(tekst)
            analyse = process_txt_file(txt_path)
            analyse_resultaten.append(analyse)
        except Exception as e:
            flash(f"Fout bij OCR-verwerking: {bestand.filename} — {e}")

    if not analyse_resultaten:
        flash("Geen bruikbare bestanden verwerkt of geen tekst herkend.")
        return render_template("ocr_upload_form.html")

    # Exporteer het eerste resultaat als test
    excel_pad = exporteer_excel(analyse_resultaten[0])
    pdf_pad = exporteer_pdf(analyse_resultaten[0])

    return render_template(
        "resultaat.html",
        resultaten=analyse_resultaten,
        excel_bestand=os.path.basename(excel_pad),
        pdf_bestand=os.path.basename(pdf_pad)
    )

@app.route("/ocr-download/<bestand>")
def ocr_download(bestand):
    return send_from_directory(EXPORT_FOLDER, bestand, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
