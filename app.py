HEAD
from flask import Flask, render_template, request, redirect, url_for, send_file, session
from weasyprint import HTML
import os
import pandas as pd
from modules.csv_parser import parse_csv
from modules.google_km import bereken_afstand_google
from datetime import datetime
from dataclasses import dataclass
import uuid

app = Flask(__name__)
app.secret_key = 'secure_routing_key_123'  # Zet dit in .env voor productie


@dataclass
class Rit:
    datum: str
    starttijd: str
    eindtijd: str
    locatie: str
    afstand_km: float


@app.route('/')
def home():
    return render_template('import/home.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        bestand = request.files['bestand']
        thuis = request.form['thuisadres']
        kantoor = request.form['kantooradres']
        bestandsnaam = bestand.filename
        uploadpad = os.path.join('uploads', bestandsnaam)
        bestand.save(uploadpad)

        if bestandsnaam.endswith('.csv'):
            ritten = parse_csv(uploadpad, thuis, kantoor)
            session['ritten'] = [rit.__dict__ for rit in ritten]
            return redirect(url_for('resultaat'))

    return render_template('import/index.html')


@app.route('/resultaat')
def resultaat():
    ritten_data = session.get('ritten')
    if not ritten_data:
        return redirect(url_for('index'))

    ritten = [Rit(**r) for r in ritten_data]
    totaal_km = sum(rit.afstand_km for rit in ritten)
    woon_werk_km = sum(rit.afstand_km for rit in ritten if "kantoor" in rit.locatie.lower())

    return render_template("import/resultaat.html", ritten=ritten, totaal=totaal_km, woonwerk=woon_werk_km)


@app.route('/download/pdf')
def download_pdf():
    ritten_data = session.get('ritten', [])
    if not ritten_data:
        return redirect(url_for('index'))

    html = render_template("import/pdf_template.html", ritten=ritten_data)
    pdf = HTML(string=html).write_pdf()
    pdfpad = f"exports/ritsync_{uuid.uuid4().hex[:8]}.pdf"

    with open(pdfpad, 'wb') as f:
        f.write(pdf)

    return send_file(pdfpad, as_attachment=True)


@app.route('/download/excel')
def download_excel():
    ritten_data = session.get('ritten', [])
    if not ritten_data:
        return redirect(url_for('index'))

    df = pd.DataFrame(ritten_data)
    excelpad = f"exports/ritsync_{uuid.uuid4().hex[:8]}.xlsx"
    df.to_excel(excelpad, index=False)

    return send_file(excelpad, as_attachment=True)


if __name__ '__main__':
=======
from flask import Flask, render_template
import os
from backend.routes.ocr_routes import ocr_routes

app = Flask(
    __name__,
    template_folder="frontend/templates",  # <--- voeg dit toe
    static_folder="frontend/static"        # optioneel, als je daar CSS/JS hebt
)
app.secret_key ="sleutel1201"

# Register OCR blueprint
app.register_blueprint(ocr_routes)

# Route voor homepage (index)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Route om OCR-uploadformulier te tonen
@app.route("/upload_ocr", methods=["GET"])
def show_ocr_form():
    return render_template("ocr_upload_form.html")

# (optioneel) Route voor resultaatpagina
@app.route("/resultaat", methods=["GET"])
def resultaat():
    return render_template("resultaat.html")

if __name__ "__main__":
    786e81ce811eea5f14fc6910c32fe7510080b6b4
    app.run(debug=True)
