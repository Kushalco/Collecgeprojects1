import pandas as pd
import os
from config import UPLOAD_FOLDER

def process_and_compare(file1, file2):
    try:
        df1 = pd.read_excel(file1, dtype={"Roll No": str})
        df2 = pd.read_excel(file2, dtype={"Roll No": str})

        # Strip whitespace from column names
        df1.columns = df1.columns.str.strip()
        df2.columns = df2.columns.str.strip()

        mismatches = []
        for _, row in df1.iterrows():
            roll_no = row.get("Roll No", None)
            if not roll_no:  # Skip invalid roll numbers
                continue

            subjects_chosen = row.get("Chosen Subjects", "Not Found")
            matched_row = df2[df2["Roll No"] == roll_no]

            if matched_row.empty:
                mismatches.append({
                    "Roll No": roll_no,
                    "Chosen": subjects_chosen,
                    "Allocated": "Not Found",
                    "Status": "Not Found"
                })
            else:
                allocated_subjects = matched_row.iloc[0].get("Allocated Subjects", "Not Found")
                status = "Mismatch" if subjects_chosen != allocated_subjects else "Match"
                mismatches.append({
                    "Roll No": roll_no,
                    "Chosen": subjects_chosen,
                    "Allocated": allocated_subjects,
                    "Status": status
                })

        return mismatches
    except Exception as e:
        return {"error": str(e)}

def get_student_subjects(roll_no):
    file1 = os.path.join(UPLOAD_FOLDER, "Enrolement_Dummy Data.xlsx")
    file2 = os.path.join(UPLOAD_FOLDER, "4th Year Elective Allocation.xlsx")

    if not os.path.exists(file1) or not os.path.exists(file2):
        return {"error": "Files not found. Please upload first!"}

    try:
        df1 = pd.read_excel(file1, dtype={"Roll No": str})
        df2 = pd.read_excel(file2, dtype={"Roll No": str})

        # Remove any whitespace from column names
        df1.columns = df1.columns.str.strip()
        df2.columns = df2.columns.str.strip()

        chosen_subjects = df1[df1["Roll No"] == roll_no]["Chosen Subjects"].values
        allocated_subjects = df2[df2["Roll No"] == roll_no]["Allocated Subjects"].values

        return {
            "Roll No": roll_no,
            "Chosen": chosen_subjects[0] if len(chosen_subjects) > 0 else "Not Found",
            "Allocated": allocated_subjects[0] if len(allocated_subjects) > 0 else "Not Found",
            "Status": "Mismatch" if len(chosen_subjects) > 0 and len(allocated_subjects) > 0 and chosen_subjects[0] != allocated_subjects[0] else "Match"
        }
    except Exception as e:
        return {"error": str(e)}
