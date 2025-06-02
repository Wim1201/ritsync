import pandas as pd
import os
from datetime import datetime

# Mapping van alias-kolomnamen → standaard
COLUMN_MAP = {
    'datum': 'datum',
    'date': 'datum',
    'tijd': 'tijd',
    'starttijd': 'tijd',
    'begin': 'tijd',
    'adres': 'adres',
    'locatie': 'adres',
    'project': 'project',
    'projectnummer': 'project'
}

# Verwachte standaardkolommen
VERWACHTE_KOLOMMEN = ['datum', 'tijd', 'adres', 'project']

def normaliseer_kolommen(columns):
    """Map kolomnamen naar gestandaardiseerde namen."""
    genormaliseerd = []
    for col in columns:
        sleutel = col.strip().lower()
        genormaliseerd.append(COLUMN_MAP.get(sleutel, sleutel))
    return genormaliseerd

def parse_csv(filepath, thuisadres=None, kantooradres=None):
    fouten = []
    ritten = []

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise Exception(f"📛 Kan CSV-bestand niet lezen: {e}")

    # Kolomnamen normaliseren
    df.columns = normaliseer_kolommen(df.columns)

    for idx, row in df.iterrows():
        try:
            if row.isnull().all():
                continue  # sla lege regels over

            rit = {
                'datum': parse_datum(row.get('datum')),
                'tijd': str(row.get('tijd')).strip(),
                'adres': str(row.get('adres')).strip(),
                'project': str(row.get('project')).strip() if 'project' in row else '',
            }

            if not rit['datum'] or not rit['adres']:
                fouten.append(f"🚫 Rij {idx+1} ontbreekt verplichte velden")
                continue

            ritten.append(rit)

        except Exception as e:
            fouten.append(f"🚫 Rij {idx+1} parsingfout: {str(e)}")

    # Fouten loggen indien aanwezig
    if fouten:
        os.makedirs("logs", exist_ok=True)
        with open("logs/parse_fouten.log", "w", encoding="utf-8") as logf:
            for fout in fouten:
                logf.write(fout + "\n")

    return ritten

def parse_datum(raw):
    """Parse datum naar standaardformaat YYYY-MM-DD"""
    if pd.isna(raw):
        return None
    try:
        return pd.to_datetime(raw).strftime('%Y-%m-%d')
    except Exception:
        return None
