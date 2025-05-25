# backend/routes/routes_pdf.py
from flask import Blueprint, request, send_file, render_template
from fpdf import FPDF
import os
import tempfile

pdf_bp = Blueprint('pdf_bp', __name__)

@pdf_bp.route('/download_pdf', methods=['POST'])
def download_pdf():
    resultaten = request.form.get('resultaten', '')
    totaal_km = request.form.get('totaal_km', '0')

    resultaten_lijst = resultaten.split(';') if resultaten else []

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="RitSync - Rittenoverzicht", ln=1, align="C")
    pdf.ln(10)

    for regel in resultaten_lijst:
        pdf.multi_cell(0, 10, txt=regel)

    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Totaal kilometers (retour): {totaal_km} km", ln=1)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        pdf.output(tmp_file.name)
        return send_file(tmp_file.name, as_attachment=True, download_name="ritsync_resultaat.pdf")
