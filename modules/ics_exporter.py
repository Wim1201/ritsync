def exporteer_ritten_van_ics_data(ritten, output_path="exports/ritten_met_afstand.csv"):
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, mode='w', newline='', encoding='utf-8') as file:
        veldnamen = ["datum", "tijd", "vertrek", "aankomst", "project", "afstand_km", "reistijd_min", "extra_locatie_ocr"]
        writer = csv.DictWriter(file, fieldnames=veldnamen)
        writer.writeheader()
        for rit in ritten:
            rit["afstand_km"] = round(rit.get("afstand_km", 0.0), 1)
            rit["reistijd_min"] = round(rit.get("reistijd_min", 0.0), 1)
            writer.writerow(rit)
