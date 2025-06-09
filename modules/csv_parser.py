import csv

def parse_csv(pad_naar_csv):
    afspraken = []

    with open(pad_naar_csv, mode='r', encoding='utf-8') as bestand:
        reader = csv.DictReader(bestand)
        for rij in reader:
            datum = rij.get("Datum", "").strip()
            tijd = rij.get("Tijd", "").strip()
            locatie = rij.get("Locatie", "").strip()

            if not (datum and tijd and locatie):
                print(f"⚠️ Onvolledige regel overgeslagen: {rij}")
                continue

            omschrijving = rij.get("Omschrijving", "").strip()
            afspraken.append({
                "datum": datum,
                "starttijd": tijd,
                "locatie": locatie,
                "omschrijving": omschrijving
            })

    print(f"✅ parse_csv: {len(afspraken)} afspraken geparsed.")
    return afspraken
