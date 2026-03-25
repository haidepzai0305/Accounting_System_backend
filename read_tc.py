import sys
def ensure_installed(package):
    import subprocess
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

ensure_installed('pandas')
ensure_installed('openpyxl')

import pandas as pd
import json

file_path = r"C:\Users\Admin\Documents\TestCases US Sign Up.xlsx"
try:
    df = pd.read_excel(file_path)
    df = df.fillna('')
    print("--- START JSON ---")
    print(json.dumps(df.to_dict('records'), indent=2))
    print("--- END JSON ---")
except Exception as e:
    print(f"Error reading Excel file: {e}")
