import pandas as pd
import os
from config import UPLOAD_FOLDER

def search_mismatches(query):
    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, "mismatches.csv"))

    if query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]

    return df.to_dict(orient="records")
