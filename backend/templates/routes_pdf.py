# backend/routes_pdf.py
from flask import Blueprint, request, send_file, jsonify
from services.pdf_service import genereer_pdf
import os
import datetime

pdf_bp = Blueprint('pdf_bp', __name__)

@pdf_bp.route("/download_pdf", methods=[POST])
def download_pdf():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "Geen data ontvangen"}), 400

        filename = f"ritsync_rapport_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        output_path = os.path.join("data/output", filename)

        genereer_pdf(data, output_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
