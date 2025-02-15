import pandas as pd
from datetime import time

TIME_FILE_PATH: str = "../config/Time.xlsx"

df = pd.read_excel(TIME_FILE_PATH, sheet_name=0, usecols="A:C")
TIME: dict[int, dict[str, time]] = {row['Tiết']: row.to_dict() for _, row in df.iterrows()}