import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def ingest_data():
    Tk().withdraw()

    file_path = askopenfilename(
        title="Select Data File",
        filetypes=[
            ("CSV files", "*.csv"),
            ("Excel files", "*.xlsx"),
            ("JSON files", "*.json")
        ]
    )

    if not file_path:
        raise ValueError("No file selected.")

    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)

    elif file_path.endswith(".json"):
        return pd.read_json(file_path)

    else:
        raise ValueError("Unsupported file format.")