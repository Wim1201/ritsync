import re
import datetime

def parse_ocr_output(ocr_text):
    afspraken = []
    regels = ocr_text.splitlines()

    for regel in regels:
        regel = regel.strip().replace("–", "-").replace("’", "'").replace("”", '"')
        if not regel:
            continue

        match = re.match(r"(\d{1,2}-\d{1,2}-\d{2,4})\s+(\d{1,2}:\d{2})\s+(.*)", regel)
        if match:
            datum_str, tijd_str, adres = match.groups()
            try:
                datumtijd = datetime.datetime.strptime(f"{datum_str} {tijd_str}", "%d-%m-%Y %H:%M")
                afspraken.append({"tijdstip": datumtijd, "adres": adres.strip()})
            except ValueError:
                continue

    return afspraken
