import pandas as pd
pd.read_json("/files/result.json").to_excel("result.xlsx")
