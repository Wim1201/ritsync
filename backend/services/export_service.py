import os
import pandas as pd
from datetime import datetime
import pdfkit
from flask import render_template_string

# Configureer pad naar wkhtmltopdf
WKHTMLTOPDF_PAD = os.path.abspath("bin/wkhtmltopdf.exe")
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PAD)

def exporteer_excel(data):
    output_folder = "data/output"
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bestandspad = os.path.join(output_folder, f"ritten_{timestamp}.xlsx")

    if isinstance(data, list) and isinstance(data[0], dict):
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame([{"data": str(data)}])

    df.to_excel(bestandspad, index=False)
    return bestandspad

def exporteer_pdf(data):
    output_folder = "data/output"
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdfpad = os.path.join(output_folder, f"ritten_{timestamp}.pdf")

    # Simpele fallback als data geen standaard structuur heeft
    if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
        data = [{"inhoud": str(data)}]

    html_template = """
    <!DOCTYPE html>
    <html lang="nl">
    <head>
        <meta charset="UTF-8">
        <title>Ritregistratie</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            table { border-collapse: collapse; width: 100%; margin-top: 20px; }
            th, td { border: 1px solid #ccc; padding: 8px; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>Ritregistratie</h1>
        <table>
            <thead>
                <tr>
                    {% for key in data[0].keys() %}
                        <th>{{ key }}</th>
                    {% endfor %}
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                    <tr>
                        {% for value in row.values() %}
                            <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """

    rendered_html = render_template_string(html_template, data=data)
    pdfkit.from_string(rendered_html, pdfpad, configuration=config)
    return pdfpad
