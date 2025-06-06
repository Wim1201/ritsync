from flask import Flask, request, render_template, redirect, url_for, session, send_file
from pathlib import Path
from werkzeug.utils import secure_filename
from backend.services.pdf_service import genereer_pdf
from backend.services.excel_service import genereer_excel

app = Flask(__name__)
app.secret_key = "geheimetestwaarde"

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

@app.route("/")
def root():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("start.html")

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/verwerk", methods=["POST"])
def verwerk():
    thuisadres = request.form.get("thuisadres")
    kantooradres = request.form.get("kantooradres")

    agenda_bestanden = request.files.getlist("agenda_files")
    ics_bestanden = request.files.getlist("ics_files")

    agenda_bestanden = [f for f in agenda_bestanden if f and f.filename]
    ics_bestanden = [f for f in ics_bestanden if f and f.filename]

    for bestand in agenda_bestanden + ics_bestanden:
        bestandsnaam = secure_filename(bestand.filename)
        bestand.save(UPLOAD_FOLDER / bestandsnaam)

    # Simulatie/mockdata voor demo
    ritgegevens = [
        {
            "datum": "2025-06-06",
            "tijd": "09:00",
            "vertrek": thuisadres,
            "bestemming": kantooradres,
            "kilometers": 27.4,
            "project": "Ritsync MVP"
        },
        {
            "datum": "2025-06-07",
            "tijd": "14:30",
            "vertrek": kantooradres,
            "bestemming": thuisadres,
            "kilometers": 27.4,
            "project": "Ritsync MVP"
        }
    ]

    session["ritgegevens"] = ritgegevens
    session["totaal_km"] = sum(r["kilometers"] for r in ritgegevens)
    session["woonwerk_km"] = 12.0  # Placeholder

    return redirect(url_for("resultaat"))

@app.route("/resultaat")
def resultaat():
    ritgegevens = session.get("ritgegevens", [])
    totaal_km = session.get("totaal_km", 0)
    woonwerk_km = session.get("woonwerk_km", 0)
    return render_template("resultaat.html", ritten=ritgegevens, totaal_km=totaal_km, woonwerk_km=woonwerk_km)

@app.route("/export/pdf")
def download_pdf():
    data = session.get("ritgegevens", [])
    if not data:
        return "<h2>Geen ritgegevens gevonden om te exporteren.</h2>", 400

    temp_pdf_path = Path("data/output/ritregistratie.pdf")
    genereer_pdf(data, temp_pdf_path)
    return send_file(temp_pdf_path, as_attachment=True)

@app.route("/export/excel")
def download_excel():
    data = session.get("ritgegevens", [])
    if not data:
        return "<h2>Geen ritgegevens gevonden om te exporteren.</h2>", 400

    pad = genereer_excel(data)
    return send_file(pad, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
