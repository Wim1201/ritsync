# modules/match_ocr_to_ics.py

def match_ocr_aan_ritten(ritten, ocr_data):
    """
    Match OCR-gegevens aan ICS-ritten op basis van projectnummer.
    """
    matched = []
    for rit in ritten:
        if rit.get("project") == ocr_data.get("project"):
            rit["extra_locatie_ocr"] = ocr_data.get("locatie")
        matched.append(rit)
    return matched
