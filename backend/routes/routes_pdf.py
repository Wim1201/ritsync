from flask import Blueprint, request, send_file, render_template
from backend.services.ritsync_service import bereken_kilometers
from backend.services.google_service import get_distance_km
import pdfkit
import tempfile
import os

pdf_route = Blueprint('pdf_route', __name__)

@pdf_route.route('/download', methods=['POST'])
def download_pdf():
    data = request.get_json()
    adressen = data.get("adressen", [])
    thuisadres = data.get("thuisadres", "")
    kantooradres = data.get("kantooradres", "")

    if not adressen or not thuisadres or not kantooradres:
        return {"error": "Invoer onvolledig"}, 400

    # Bereken ketens, afstanden en waarschuwingen
    ketens, keten_afstanden, totaal_km, waarschuwingen = bereken_kilometers(
        adressen,
        get_distance_km,
        thuisadres,
        kantooradres
    )

    rendered = render_template(
        "pdf_template.html",
        ketens=ketens,
        keten_afstanden=keten_afstanden,
        totaal_km=totaal_km,
        waarschuwingen=waarschuwingen,
        thuisadres=thuisadres,
        kantooradres=kantooradres
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        pdfkit.from_string(rendered, tmp.name)
        return send_file(tmp.name, as_attachment=True, download_name="ritregistratie.pdf")
