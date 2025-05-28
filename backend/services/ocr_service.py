def verwerk_upload(filepath):
    # Dummyversie
    return [{"afspraak": "Voorbeeld", "datum": "2025-05-29", "kilometers": 15}]
def verwerk_upload(pad_naar_bestand):
    with open(pad_naar_bestand, 'r', encoding='utf-8') as f:
        return f.read()
