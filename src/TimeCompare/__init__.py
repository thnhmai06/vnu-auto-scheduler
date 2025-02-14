import pandas as pd
from datetime import time

df = pd.read_excel("config/Time.xlsx", sheet_name=0, usecols="A:C")
df.set_index(df.columns[0], inplace=True)
TIME: list[dict[str, time]] = df.to_dict(orient="records")