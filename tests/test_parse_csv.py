from modules.csv_parser import parse_csv

print("🧪 Start test vernieuwde parse_csv()...")

bestand = "tests/test_ritten.csv"  # Zorg dat dit bestand bestaat

try:
    ritten = parse_csv(bestand)
    print(f"✅ Aantal geparste ritten: {len(ritten)}")
    for rit in ritten:
        print(f"📅 {rit['datum']} | 🕒 {rit['tijd']} | 📍 {rit['adres']} | 🔢 {rit.get('project', '')}")
except Exception as e:
    print(f"❌ Parserfout: {e}")


