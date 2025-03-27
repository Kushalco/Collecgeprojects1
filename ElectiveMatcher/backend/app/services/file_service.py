import pandas as pd
import os
from config import UPLOAD_FOLDER

def process_and_compare(file1, file2):
    # Read CSV with encoding fix
    df1 = pd.read_csv(file1, encoding="utf-8", errors="replace", engine="python")
    df2 = pd.read_csv(file2, encoding="utf-8", errors="replace", engine="python")

    mismatches = []
    for _, row in df1.iterrows():
        roll_no = row["Roll No"]
        subjects_chosen = str(row["Chosen Subjects"]).strip()  # Ensure it’s a string

        matched_row = df2[df2["Roll No"] == roll_no]
        if matched_row.empty:
            mismatches.append({"Roll No": roll_no, "Chosen": subjects_chosen, "Allocated": "Not Found", "Status": "Not Found"})
        else:
            allocated_subjects = str(matched_row.iloc[0]["Allocated Subjects"]).strip()
            if subjects_chosen != allocated_subjects:
                mismatches.append({"Roll No": roll_no, "Chosen": subjects_chosen, "Allocated": allocated_subjects, "Status": "Mismatch"})

    return mismatches

def get_student_subjects(roll_no):
    try:
        df1 = pd.read_csv(os.path.join(UPLOAD_FOLDER, "elective_choices.csv"), encoding="utf-8", errors="replace", engine="python")
        df2 = pd.read_csv(os.path.join(UPLOAD_FOLDER, "allocated_subjects.csv"), encoding="utf-8", errors="replace", engine="python")

        chosen_subjects = df1.loc[df1["Roll No"] == roll_no, "Chosen Subjects"].astype(str).values
        allocated_subjects = df2.loc[df2["Roll No"] == roll_no, "Allocated Subjects"].astype(str).values

        return {
            "Roll No": roll_no,
            "Chosen": chosen_subjects[0] if len(chosen_subjects) > 0 else "Not Found",
            "Allocated": allocated_subjects[0] if len(allocated_subjects) > 0 else "Not Found",
            "Status": "Mismatch" if chosen_subjects.tolist() != allocated_subjects.tolist() else "Match"
        }
    except Exception as e:
        return {"error": str(e)}
