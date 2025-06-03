# run_ics_to_csv.py

from modules.ics_to_csv import ics_to_csv

# Pas dit pad aan naar jouw .ics testbestand
ics_input = "import/sample.ics"

# Optioneel: specificeer ander pad voor de export
output_path = ics_to_csv(ics_input)

print(f"CSV gegenereerd: {output_path}")
