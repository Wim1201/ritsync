from flask import Blueprint, request, render_template, make_response, current_app
import pdfkit
import os
import uuid
import traceback

# Blueprint aanmaken
pdf_bp = Blueprint('pdf_bp', __name__)

@pdf_bp.route('/download_pdf', methods=['POST'])
def download_pdf():
    try:
        locatie = request.form.get('locatie', 'Onbekend')
        totaal_km = request.form.get('totaal_km', 'n.v.t.')
        co2 = request.form.get('co2', 'n.v.t.')
        declarabel = request.form.get('declarabel', 'n.v.t.')

        print("📄 PDF wordt gegenereerd voor:")
        print(f"  Locatie: {locatie}, KM: {totaal_km}, CO2: {co2}, Declarabel: {declarabel}")

        # HTML renderen uit template
        rendered = render_template(
            'pdf_template.html',
            locatie=locatie,
            totaal_km=totaal_km,
            co2=co2,
            declarabel=declarabel
        )

        # Tijdelijke HTML genereren
        bestandsnaam = f"ritsync_{uuid.uuid4().hex[:8]}.pdf"
        temp_html = os.path.join(current_app.root_path, f'temp_{bestandsnaam}.html')
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(rendered)

        # PDF genereren met wkhtmltopdf
        config = pdfkit.configuration(wkhtmltopdf=os.getenv('WKHTMLTOPDF_PATH', 'wkhtmltopdf'))
        pdf_output = pdfkit.from_file(temp_html, False, configuration=config)

        os.remove(temp_html)

        response = make_response(pdf_output)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={bestandsnaam}'
        return response

    except Exception as e:
        print("🚨 Fout bij PDF-generatie:")
        traceback.print_exc()
        return f"Fout bij het genereren van de PDF: {str(e)}", 500
