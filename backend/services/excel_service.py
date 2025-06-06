import os
import pandas as pd
from datetime import datetime
from pathlib import Path

def genereer_excel(data):
    output_folder = Path("data/output")
    output_folder.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bestandspad = output_folder / f"ritten_{timestamp}.xlsx"

    if isinstance(data, list) and isinstance(data[0], dict):
        df = pd.DataFrame(data)
    else:
        df = pd.DataFrame([{"data": str(data)}])

    df.to_excel(bestandspad, index=False)
    return str(bestandspad)
