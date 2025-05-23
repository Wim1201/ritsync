import requests

data = {
    "periode": "januari 2025",
    "totaal_km": 910,
    "verbruik_liter": 91,
    "vergoeding": "207,45",
    "ritten": [
        {"datum": "2025-01-07", "van": "Dongen", "naar": "Tilburg", "afstand": 20},
        {"datum": "2025-01-08", "van": "Tilburg", "naar": "Dongen", "afstand": 20}
    ]
}

response = requests.post("http://localhost:5000/download_pdf", json=data)

if response.status_code == 200:
    with open("ritsync_rapport_test.pdf", "wb") as f:
        f.write(response.content)
    print("PDF succesvol gedownload!")
else:
    print("Fout:", response.text)
