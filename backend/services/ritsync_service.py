import datetime

def bereken_kilometers(adressen, afstandsfunctie, thuisadres, kantooradres, interval_minuten=120):
    ketens = []
    huidige_keten = []
    vorige_adres = thuisadres
    vorige_tijd = None

    for afspraak in adressen:
        if not isinstance(afspraak, dict):
            continue

        huidig_adres = afspraak.get("adres")
        huidig_tijdstip = afspraak.get("tijdstip")

        if not huidig_adres or not huidig_tijdstip or not isinstance(huidig_tijdstip, datetime.datetime):
            continue

        if vorige_tijd is None:
            huidige_keten = [thuisadres, huidig_adres]
        else:
            tijdverschil = (huidig_tijdstip - vorige_tijd).total_seconds() / 60
            if tijdverschil > interval_minuten:
                afstand_kantoor = afstandsfunctie(huidig_adres, kantooradres)
                afstand_thuis = afstandsfunctie(huidig_adres, thuisadres)
                eindpunt = kantooradres if afstand_kantoor < afstand_thuis else thuisadres
                huidige_keten.append(eindpunt)
                ketens.append(huidige_keten)
                startpunt = kantooradres if eindpunt == thuisadres else thuisadres
                huidige_keten = [startpunt, huidig_adres]
            else:
                huidige_keten.append(huidig_adres)

        vorige_adres = huidig_adres
        vorige_tijd = huidig_tijdstip

    if huidige_keten:
        afstand_kantoor = afstandsfunctie(huidige_keten[-1], kantooradres)
        afstand_thuis = afstandsfunctie(huidige_keten[-1], thuisadres)
        eindpunt = kantooradres if afstand_kantoor < afstand_thuis else thuisadres
        huidige_keten.append(eindpunt)
        ketens.append(huidige_keten)

    totalen = []
    for keten in ketens:
        totaal_km = 0.0
        for i in range(len(keten) - 1):
            afstand = afstandsfunctie(keten[i], keten[i + 1])
            totaal_km += afstand
        totalen.append(round(totaal_km, 2))

    return ketens, totalen
