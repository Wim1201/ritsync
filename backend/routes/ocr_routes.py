from flask import Blueprint, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
from backend.services.ocr_service import extract_text_from_file

ocr_routes = Blueprint('ocr_routes', __name__)

UPLOAD_FOLDER = 'ritsync/data/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@ocr_routes.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Geen bestand meegegeven.')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('Geen bestand geselecteerd.')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(upload_path)

        try:
            extract_text_from_file(upload_path)
            flash('Bestand succesvol verwerkt.')
        except Exception as e:
            flash(f'OCR-verwerking mislukt: {e}')

        return redirect(url_for('index'))

    else:
        flash('Ongeldig bestandstype. Alleen PNG, JPG, JPEG of PDF toegestaan.')
        return redirect(url_for('index'))
