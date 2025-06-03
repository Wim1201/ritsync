import os
import threading
import webbrowser
from flask import Flask, request, redirect, render_template, send_file
from werkzeug.utils import secure_filename

# Modules
from modules.ics_parser import parse_ics
from modules.ics_exporter import exporteer_ritten_van_ics_data
from modules.ocr_reader import lees_tekst_van_bestand, extract_project_info
from modules.match_ocr_to_ics import match_ocr_aan_ritten

# Flask setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
EXPORT_FILE = 'exports/ritten_met_afstand.csv'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('exports', exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
@app.route('/upload', methods=['POST'])
def upload():
    ics_file = request.files.get('ics_file')
    ocr_files = request.files.getlist('ocr_files')  # ✅ meerdere OCR-bestanden

    ritten = []

    # ICS verwerken als aanwezig
    if ics_file and ics_file.filename != '':
        ics_path = os.path.join(UPLOAD_FOLDER, secure_filename(ics_file.filename))
        ics_file.save(ics_path)
        ritten = parse_ics(ics_path)
    else:
        ritten = []  # Geen ICS = lege rittenlijst (OCR-only mode)

    # OCR verwerken
    if ocr_files:
        for ocr_file in ocr_files:
            if ocr_file.filename == '':
                continue
            ocr_path = os.path.join(UPLOAD_FOLDER, secure_filename(ocr_file.filename))
            ocr_file.save(ocr_path)
            tekst = lees_tekst_van_bestand(ocr_path)
            ocr_data = extract_project_info(tekst)

            # Bij ICS aanwezig: match met ritten
            if ritten:
                ritten = match_ocr_aan_ritten(ritten, ocr_data)
            else:
                # OCR-only rit bouwen
                ritten.append({
                    "datum": "",  # optioneel leeg laten
                    "tijd": "",
                    "vertrek": "",
                    "aankomst": "",
                    "project": ocr_data.get("project"),
                    "extra_locatie_ocr": ocr_data.get("locatie")
                })

    # CSV exporteren
    exporteer_ritten_van_ics_data(ritten)
    return redirect("/download")

@app.route('/download')
def download():
    return render_template('download.html')

@app.route('/export')
def export_csv():
    return send_file(EXPORT_FILE, as_attachment=True)

# Automatisch openen in browser
if __name__ == '__main__':
    def open_browser():
        webbrowser.open("http://127.0.0.1:5000")
    threading.Timer(1, open_browser).start()
    app.run(host="0.0.0.0", port=10000, debug=True)

