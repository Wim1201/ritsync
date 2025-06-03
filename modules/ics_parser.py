# modules/ics_parser.py

from datetime import datetime
import re

def parse_ics(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    events = []
    event = {}
    inside_event = False

    for line in lines:
        line = line.strip()

        if line == "BEGIN:VEVENT":
            event = {}
            inside_event = True

        elif line == "END:VEVENT" and inside_event:
            events.append(event)
            event = {}
            inside_event = False

        elif inside_event:
            if line.startswith("DTSTART"):
                raw_datetime = line.split(":")[1]
                dt = datetime.strptime(raw_datetime, "%Y%m%dT%H%M%S")
                event["datum"] = dt.strftime("%Y-%m-%d")
                event["tijd"] = dt.strftime("%H:%M")

            elif line.startswith("LOCATION:"):
                loc = line.replace("LOCATION:", "").strip()
                if "->" in loc:
                    vertrek, aankomst = map(str.strip, loc.split("->"))
                elif "→" in loc:
                    vertrek, aankomst = map(str.strip, loc.split("→"))
                else:
                    vertrek = aankomst = loc
                event["vertrek"] = vertrek
                event["aankomst"] = aankomst

            elif line.startswith("SUMMARY:"):
                summary = line.replace("SUMMARY:", "").strip()
                project_match = re.search(r"\b(\d{3,})\b", summary)
                if project_match:
                    event["project"] = project_match.group(1)

    return events
