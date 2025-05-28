import sys
import os
from flask import Flask, render_template
from dotenv import load_dotenv  # ➕ toegevoegd

# 🔃 .env laden
load_dotenv()
print("✅ Gekozen wkhtmltopdf-pad:", os.getenv("WKHTMLTOPDF_PATH"))

# Voeg backend-map toe aan het pad voor import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.routes.routes_pdf import pdf_bp
from backend.routes.ocr_upload_route import ocr_bp

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.secret_key = 'sleutel1201'

# Blueprints registreren
app.register_blueprint(pdf_bp)
app.register_blueprint(ocr_bp)

@app.route("/")
def index():
    return render_template("upload_form.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)



