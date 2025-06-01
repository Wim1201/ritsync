import datetime

def bereken_kilometers(adressen, afstandsfunctie, thuisadres, kantooradres):
    ketens = []
    huidige_keten = []
    waarschuwingen = []
    totaal_zakelijke_km = 0.0

    vorige_adres = thuisadres

    for afspraak in adressen:
        if not isinstance(afspraak, dict):
            continue

        adres = afspraak.get("adres")
        rit_type = afspraak.get("type", "onbekend").lower()

        if not adres:
            continue

        if rit_type == "privé":
            waarschuwingen.append(f"Privéafspraak genegeerd: {adres}")
            continue

        if rit_type != "zakelijk":
            waarschuwingen.append(f"Onbekend type afspraak bij {adres}, controleer invoer")
            continue

        if not huidige_keten:
            huidige_keten = [thuisadres, adres]
        else:
            huidige_keten.append(adres)

        vorige_adres = adres

    # Sluit keten altijd af met huis of kantoor, afhankelijk van afstand
    if huidige_keten:
        laatste_adres = huidige_keten[-1]
        afstand_kantoor = afstandsfunctie(laatste_adres, kantooradres)
        afstand_thuis = afstandsfunctie(laatste_adres, thuisadres)
        eindpunt = kantooradres if afstand_kantoor < afstand_thuis else thuisadres
        huidige_keten.append(eindpunt)
        ketens.append(huidige_keten)

    # Bereken kilometers per keten
    keten_afstanden = []
    for keten in ketens:
        totaal_km = 0.0
        for i in range(len(keten) - 1):
            afstand = afstandsfunctie(keten[i], keten[i + 1])
            totaal_km += afstand
        keten_afstanden.append(round(totaal_km, 2))
        totaal_zakelijke_km += totaal_km

    return ketens, keten_afstanden, round(totaal_zakelijke_km, 2), waarschuwingen
