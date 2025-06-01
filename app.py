from flask import Flask
from backend.routes.ocr_routes import ocr_bp
from backend.routes.routes_pdf import pdf_route  # indien van toepassing, anders weglaten

app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")
app.secret_key = "geheime_sleutel"

# Registreren van Blueprints
app.register_blueprint(ocr_bp)
app.register_blueprint(pdf_route)  # weglaten als niet van toepassing

@app.route("/")
def index():
    return "RitSync draait – gebruik /ocr-uploadpagina voor OCR-upload."

if __name__ == "__main__":
    app.run(debug=True)
