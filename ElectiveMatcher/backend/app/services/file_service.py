import pandas as pd
import os
from config import UPLOAD_FOLDER

def process_and_compare(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    mismatches = []
    for _, row in df1.iterrows():
        roll_no = row.get("Roll No", None)
        if roll_no is None:
            continue  # Skip rows without Roll No

        subjects_chosen = row["Chosen Subjects"]
        matched_row = df2[df2["Roll No"] == roll_no]

        if matched_row.empty:
            mismatches.append({
                "Roll No": roll_no,
                "Chosen": subjects_chosen,
                "Allocated": "Not Found",
                "Status": "Not Found"
            })
        else:
            allocated_subjects = matched_row.iloc[0]["Allocated Subjects"]
            if subjects_chosen != allocated_subjects:
                mismatches.append({
                    "Roll No": roll_no,
                    "Chosen": subjects_chosen,
                    "Allocated": allocated_subjects,
                    "Status": "Mismatch"
                })

    return mismatches
