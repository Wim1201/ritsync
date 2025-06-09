from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import csv
from backend.services.pdf_service import genereer_pdf
from backend.services.excel_service import genereer_excel

app = Flask(__name__)
app.secret_key = 'supersecret'

UPLOAD_FOLDER = 'uploads'
EXPORT_FOLDER = 'export'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EXPORT_FOLDER'] = EXPORT_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 📄 Home
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# 📤 Upload CSV
@app.route('/verwerk', methods=['POST'])
def verwerk():
    if 'bestand' not in request.files:
        flash("Geen bestand geselecteerd.")
        return redirect(request.url)

    bestand = request.files['bestand']
    if bestand.filename == '':
        flash("Geen bestandsnaam opgegeven.")
        return redirect(request.url)

    if bestand and allowed_file(bestand.filename):
        bestand_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_upload.csv')
        bestand.save(bestand_path)
        flash("➡️ Bestand ontvangen en opgeslagen")
        return redirect(url_for('resultaat'))

    flash("⚠️ Ongeldig bestandstype. Alleen .csv toegestaan.")
    return redirect(request.url)


# 📊 Resultaat tonen
@app.route('/resultaat')
def resultaat():
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_upload.csv')
    ritten = []
    totaal_km = 0.0
    woonwerk_km = 0.0

    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for rij in reader:
                locatie = rij.get('Locatie', '').strip()
                datum = rij.get('Datum', '').strip()
                tijd = rij.get('Tijd', '').strip()
                km = float(rij.get('Kilometers', 0) or 0)
                omschrijving = rij.get('Omschrijving', '').strip()

                if not locatie or not datum or not tijd:
                    flash(f"⚠️ Onvolledige regel overgeslagen: {rij}")
                    continue

                ritten.append({
                    'Datum': datum,
                    'Tijd': tijd,
                    'Locatie': locatie,
                    'Omschrijving': omschrijving,
                    'Kilometers': km
                })

                totaal_km += km
                # 💡 woonwerk km logica kun je hier uitbreiden

    flash(f"✅ Geparsed: {len(ritten)} items")
    return render_template('resultaat.html', ritten=ritten, totaal_km=totaal_km, woonwerk_km=woonwerk_km)


# 🧾 Exporteer naar PDF
@app.route('/export/pdf')
def exporteer_pdf():
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_upload.csv')
    ritten, totaal_km, woonwerk_km = laad_ritten(csv_path)
    bestandsnaam = genereer_pdf(ritten, totaal_km, woonwerk_km)
    return send_file(bestandsnaam, as_attachment=True)


# 📊 Exporteer naar Excel
@app.route('/export/excel')
def exporteer_excel():
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_upload.csv')
    ritten, totaal_km, woonwerk_km = laad_ritten(csv_path)
    bestandsnaam = genereer_excel(ritten, totaal_km, woonwerk_km)
    return send_file(bestandsnaam, as_attachment=True)


# 🔁 Hergebruikbare CSV parser
def laad_ritten(pad):
    ritten = []
    totaal_km = 0.0
    woonwerk_km = 0.0

    if os.path.exists(pad):
        with open(pad, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for rij in reader:
                locatie = rij.get('Locatie', '').strip()
                datum = rij.get('Datum', '').strip()
                tijd = rij.get('Tijd', '').strip()
                km = float(rij.get('Kilometers', 0) or 0)
                omschrijving = rij.get('Omschrijving', '').strip()

                if not locatie or not datum or not tijd:
                    continue

                ritten.append({
                    'Datum': datum,
                    'Tijd': tijd,
                    'Locatie': locatie,
                    'Omschrijving': omschrijving,
                    'Kilometers': km
                })

                totaal_km += km

    return ritten, totaal_km, woonwerk_km


if __name__ == '__main__':
    app.run(debug=True)
