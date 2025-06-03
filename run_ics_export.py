# run_ics_export.py

from modules.ics_exporter import exporteer_ritten_van_ics

pad = exporteer_ritten_van_ics("import/calendar.ics")
print(f"✅ Ritten geëxporteerd naar: {pad}")
