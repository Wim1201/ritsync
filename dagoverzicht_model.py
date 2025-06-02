# dagoverzicht_model.py
class Rit:
    def __init__(self, starttijd, eindtijd, van, naar, type, afstand_km, project=None):
        self.starttijd = starttijd
        self.eindtijd = eindtijd
        self.van = van
        self.naar = naar
        self.type = type
        self.afstand_km = afstand_km
        self.project = project

class Dagoverzicht:
    def __init__(self, datum, ritten):
        self.datum = datum
        self.ritten = ritten
        self.totaal_km = sum(r.afstand_km for r in ritten)
        self.woonwerk_km = sum(r.afstand_km for r in ritten if r.type == "Woon-Werk")

def get_simulatie_dagen():
    return [
        Dagoverzicht("2025-06-01", [
            Rit("08:30", "09:00", "Thuis", "Kantoor", "Woon-Werk", 10),
            Rit("09:30", "11:00", "Kantoor", "Tilburg", "Zakelijk", 18),
            Rit("14:00", "15:00", "Tilburg", "Thuis", "Zakelijk", 19),
        ]),
        Dagoverzicht("2025-06-02", [
            Rit("07:45", "08:15", "Thuis", "Eindhoven", "Zakelijk", 40, "1002"),
            Rit("10:00", "11:00", "Eindhoven", "Kantoor", "Zakelijk", 22),
            Rit("12:00", "13:00", "Kantoor", "Thuis", "Woon-Werk", 20),
        ]),
        Dagoverzicht("2025-06-03", [
            Rit("09:00", "10:30", "Thuis", "Rotterdam", "Zakelijk", 75, "1003"),
            Rit("12:30", "14:00", "Rotterdam", "Thuis", "Zakelijk", 75),
        ])
    ]
