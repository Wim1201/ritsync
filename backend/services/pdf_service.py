# backend/services/pdf_service.py
import pdfkit
import os
from jinja2 import Environment, FileSystemLoader


def genereer_pdf(data, output_path):
    # Zet het pad naar de templates-map
    template_dir = os.path.join(os.path.dirname(__file__), '../templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("pdf_template.html")

    # Render de HTML met de opgegeven data
    html_content = template.render(data=data)

    # Zet de config voor wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=os.getenv("WKHTMLTOPDF_PATH", "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"))

    # Genereer de PDF
    pdfkit.from_string(html_content, output_path, configuration=config)
    return output_path
