# app.py (verplaatst naar hoofdmap)
from flask import Flask, render_template, request, redirect, url_for
from backend.routes.routes_pdf import pdf_bp
import os

app = Flask(__name__, template_folder="frontend/templates")
# Registreer de blueprint voor PDF-download
app.register_blueprint(pdf_bp)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "Geen bestand gevonden.", 400

    file = request.files["file"]

    if file.filename == "":
        return "Geen bestandsnaam opgegeven.", 400

    upload_map = os.path.join("backend", "uploads")
    os.makedirs(upload_map, exist_ok=True)
    opslagpad = os.path.join(upload_map, file.filename)
    file.save(opslagpad)

    print(f"Bestand opgeslagen op: {opslagpad}")
    return f"Bestand succesvol geüpload naar: {opslagpad}"

if __name__ == "__main__":
    print("=== Start app.py ===")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)


