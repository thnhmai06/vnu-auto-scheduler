import pandas as pd
from datetime import time

TIME_FILE_PATH: str = "config/Time.xlsx"

df = pd.read_excel(TIME_FILE_PATH, sheet_name=0, usecols="A:C")
df.set_index(df.columns[0], inplace=True)
TIME: list[dict[str, time]] = df.to_dict(orient="records")