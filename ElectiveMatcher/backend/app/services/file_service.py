import pandas as pd
import os
from config import UPLOAD_FOLDER

def process_and_compare(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    mismatches = []
    for _, row in df1.iterrows():
        roll_no = row["Roll No"]
        subjects_chosen = row["Chosen Subjects"]
        
        matched_row = df2[df2["Roll No"] == roll_no]
        if matched_row.empty:
            mismatches.append({"Roll No": roll_no, "Chosen": subjects_chosen, "Allocated": "Not Found", "Status": "Not Found"})
        else:
            allocated_subjects = matched_row.iloc[0]["Allocated Subjects"]
            if subjects_chosen != allocated_subjects:
                mismatches.append({"Roll No": roll_no, "Chosen": subjects_chosen, "Allocated": allocated_subjects, "Status": "Mismatch"})

    return mismatches

def get_student_subjects(roll_no):
    try:
        df1 = pd.read_csv(os.path.join(UPLOAD_FOLDER, "elective_choices.csv"))
        df2 = pd.read_csv(os.path.join(UPLOAD_FOLDER, "allocated_subjects.csv"))

        chosen_subjects = df1[df1["Roll No"] == roll_no]["Chosen Subjects"].values
        allocated_subjects = df2[df2["Roll No"] == roll_no]["Allocated Subjects"].values

        return {
            "Roll No": roll_no,
            "Chosen": chosen_subjects[0] if chosen_subjects else "Not Found",
            "Allocated": allocated_subjects[0] if allocated_subjects else "Not Found",
            "Status": "Mismatch" if chosen_subjects != allocated_subjects else "Match"
        }
    except Exception as e:
        return {"error": str(e)}
