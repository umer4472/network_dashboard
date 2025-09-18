import pandas as pd
from pathlib import Path

# Get path relative to this script
BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data.xlsx"

def load_data():
    return pd.read_excel(DATA_PATH)
