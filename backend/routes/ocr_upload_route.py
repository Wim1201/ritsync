from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename

ocr_bp = Blueprint("ocr_bp", __name__)

UPLOAD_FOLDER = os.path.join("uploads")
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ocr_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@ocr_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        flash("Geen bestand meegegeven")
        return redirect(url_for("ocr_bp.home"))

    file = request.files["file"]
    if file.filename == "":
        flash("Geen bestand geselecteerd")
        return redirect(url_for("ocr_bp.home"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # ➕ OCR-verwerking en afstandsberekening komt hier
        flash(f"Bestand succesvol geüpload: {filename}")
        return redirect(url_for("ocr_bp.home"))

    flash("Ongeldig bestandstype")
    return redirect(url_for("ocr_bp.home"))
