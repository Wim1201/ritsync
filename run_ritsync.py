from backend.services.ritsync_service import run_ritsync

# Geef hier de OCR-bestanden op die je wilt verwerken
bestandspad_lijst = [
    "C:/Users/Wim/Documents/agenda Willem/agendas jpg/Weekagenda-22052025_1125 (1)-1.txt",
    "C:/Users/Wim/Documents/agenda Willem/agendas jpg/Weekagenda-22052025_1125 (1)-2.txt"
]

run_ritsync(
    txt_files=bestandspad_lijst,
    export_excel=True,
    export_pdf=True
)
