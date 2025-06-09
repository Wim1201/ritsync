from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
from datetime import datetime

def genereer_pdf(ritten, totaal_km, woonwerk_km):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("pdf_template.html")

    html = template.render(ritgegevens=ritten, totaal_km=totaal_km, woonwerk_km=woonwerk_km)
    bestandsnaam = f"export/ritregistratie_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

    config = pdfkit.configuration(wkhtmltopdf=os.getenv("WKHTMLTOPDF_PATH", "bin/wkhtmltopdf.exe"))
    pdfkit.from_string(html, bestandsnaam, configuration=config)

    return bestandsnaam
