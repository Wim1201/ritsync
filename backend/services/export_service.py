import os
import openpyxl
from fpdf import FPDF
from datetime import datetime

EXPORTMAP = "data/output"
os.makedirs(EXPORTMAP, exist_ok=True)

def exporteer_excel(analyse):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "RitSync"
    ws.append(["Bestandsnaam", "Adres", "Categorie", "Afstand (km)"])

    totaal_km = 0.0
    totaal_woonwerk = 0.0

    for item in analyse:
        bestandsnaam = os.path.basename(item["bestand"])
        for rit in item["resultaten"]:
            ws.append([bestandsnaam, rit["adres"], rit["categorie"], rit["afstand_km"]])
        totaal_km += item.get("km_totaal", 0.0)
        totaal_woonwerk += item.get("km_woonwerk", 0.0)

    ws.append([])
    ws.append(["Totaal kilometers:", round(totaal_km, 2)])
    ws.append(["Waarvan woon-werk:", round(totaal_woonwerk, 2)])

    pad = os.path.join(EXPORTMAP, f"ocr_export_{timestamp()}.xlsx")
    wb.save(pad)
    return pad

def exporteer_pdf(analyse):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="OCR Resultaten RitSync", ln=1, align="C")
    pdf.ln(10)

    totaal_km = 0.0
    totaal_woonwerk = 0.0

    for item in analyse:
        bestandsnaam = os.path.basename(item["bestand"])
        pdf.set_font("Arial", "B", size=11)
        pdf.cell(200, 10, txt=f"Bestand: {bestandsnaam}", ln=1)
        pdf.set_font("Arial", size=10)
        for rit in item["resultaten"]:
            lijn = f"{rit['categorie'].capitalize()} | {rit['adres']} | {rit['afstand_km']} km"
            pdf.cell(200, 8, txt=lijn[:100], ln=1)
        pdf.ln(5)
        totaal_km += item.get("km_totaal", 0.0)
        totaal_woonwerk += item.get("km_woonwerk", 0.0)

    pdf.set_font("Arial", "B", size=11)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Totaal kilometers: {round(totaal_km, 2)} km", ln=1)
    pdf.cell(200, 10, txt=f"Waarvan woon-werk: {round(totaal_woonwerk, 2)} km", ln=1)

    pad = os.path.join(EXPORTMAP, f"ocr_export_{timestamp()}.pdf")
    pdf.output(pad)
    return pad

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
