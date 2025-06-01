from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import webbrowser
import threading

# Padinstellingen voor templates en static
base_dir = os.path.dirname(__file__)
template_dir = os.path.join(base_dir, 'frontend', 'templates')
static_dir = os.path.join(base_dir, 'frontend', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# === Homepage ===
@app.route("/")
def homepage():
    return render_template("homepage.html")

# === Uploadpagina (index.html) ===
@app.route("/index", methods=["GET", "POST"])
def ocr_uploadpagina():
    if request.method == "POST":
        # Tijdelijk testgedrag
        return redirect(url_for("resultaat"))
    return render_template("index.html")

# === Resultatenpagina (met dummydata) ===
@app.route("/resultaat")
def resultaat():
    ketens = [
        {"stops": ["Startadres", "Klant A", "Klant B"], "totaal_km": 42},
        {"stops": ["Startadres", "Klant C", "Klant D"], "totaal_km": 28}
    ]
    totaal_zakelijke_km = 70
    waarschuwingen = ["Controleer uw agenda op hiaten."]
    return render_template("resultaat.html", ketens=ketens, totaal_zakelijke_km=totaal_zakelijke_km, waarschuwingen=waarschuwingen)

# === PDF-download (testbestand) ===
@app.route("/download/pdf")
def download_pdf():
    return send_file("data/output/ritsync_20250525_092758.pdf", as_attachment=True)

# === Excel-download (testbestand) ===
@app.route("/download/excel")
def download_excel():
    return send_file("data/output/ritsync_20250525_092758.xlsx", as_attachment=True)

# === Automatisch browser openen ===
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# === Applicatie starten ===
if __name__ == "__main__":
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
