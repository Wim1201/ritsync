HEAD
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request, flash, send_from_directory

from flask import Flask, render_template, request, flash, send_from_directory
import os
f611f73 (Herstelde werkende versie van RitSync na rollback)
from backend.services.ocr_service import ocr_afbeelding, process_txt_file
from backend.services.export_service import exporteer_excel, exporteer_pdf

app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")
HEAD
app.secret_key = "geheime_sleutel_voor_flash_berichten"

app.secret_key = "geheime_sleutel_voor_flash"

f611f73 (Herstelde werkende versie van RitSync na rollback)
UPLOAD_FOLDER = "backend/uploads"
EXPORT_FOLDER = "data/output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)

HEAD
TOEGESTANE_EXTENSIES = {"jpg", "jpeg", "png", "pdf"}

TOEGESTANE_EXTENSIES = {"png", "jpg", "jpeg", "pdf"}
f611f73 (Herstelde werkende versie van RitSync na rollback)

def extensie_toegestaan(bestandsnaam):
    return '.' in bestandsnaam and bestandsnaam.rsplit('.', 1)[1].lower() in TOEGESTANE_EXTENSIES

HEAD

@app.route("/")
def index():
    return render_template("index.html")

f611f73 (Herstelde werkende versie van RitSync na rollback)
@app.route("/ocr-uploadpagina", methods=["GET"])
def ocr_uploadpagina():
    return render_template("ocr_upload_form.html")

@app.route("/ocr-upload", methods=["POST"])
def ocr_upload():
    if "files" not in request.files:
        flash("Geen bestanden ontvangen.")
        return render_template("ocr_upload_form.html")

    bestanden = request.files.getlist("files")
HEAD
    analyse = []

    resultaten = []
f611f73 (Herstelde werkende versie van RitSync na rollback)

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
HEAD
            tijdelijk_txtpad = bestandspad + ".txt"
            with open(tijdelijk_txtpad, "w", encoding="utf-8") as f:
                f.write(tekst)
            analyse.append(process_txt_file(tijdelijk_txtpad))
        except Exception as e:
            flash(f"Fout bij OCR-verwerking: {bestand.filename} — {e}")

    if not analyse:
        flash("Geen bruikbare bestanden verwerkt of geen tekst herkend.")
        return render_template("ocr_upload_form.html")

    excel_pad = exporteer_excel(analyse)
    pdf_pad = exporteer_pdf(analyse)

            txt_path = bestandspad + ".txt"
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(tekst)
            analyse = process_txt_file(txt_path)
            resultaten.append(analyse)
        except Exception as e:
            flash(f"Fout bij OCR-verwerking: {bestand.filename} — {e}")

    if not resultaten:
        flash("Geen bruikbare bestanden verwerkt of geen tekst herkend.")
        return render_template("ocr_upload_form.html")

    # Genereer exportbestanden
    excel_pad = exporteer_excel(resultaten[0])
    pdf_pad = exporteer_pdf(resultaten[0])
f611f73 (Herstelde werkende versie van RitSync na rollback)

    excel_bestand = os.path.basename(excel_pad)
    pdf_bestand = os.path.basename(pdf_pad)

HEAD
    return render_template("resultaat.html", resultaten=analyse, excel_bestand=excel_bestand, pdf_bestand=pdf_bestand)

    return render_template("resultaat.html", resultaten=resultaten, excel_bestand=excel_bestand, pdf_bestand=pdf_bestand)
f611f73 (Herstelde werkende versie van RitSync na rollback)

@app.route("/ocr-download/<bestand>")
def ocr_download(bestand):
    return send_from_directory(EXPORT_FOLDER, bestand, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
