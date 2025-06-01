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

if __name__ == "__main__":
    app.run(debug=True)
