import pandas as pd
import os
from config import UPLOAD_FOLDER

def process_and_compare(file1, file2):
    # Read XLSX files
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Print column names for debugging
    print("Columns in file1:", df1.columns.tolist())
    print("Columns in file2:", df2.columns.tolist())

    # Standardizing column names (removing leading/trailing spaces)
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    mismatches = []
    for _, row in df1.iterrows():
        roll_no = row.get("Roll No", None)  # Use .get() to avoid crashes

        if roll_no is None:
            continue  # Skip rows with missing Roll No

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
        df1 = pd.read_excel(os.path.join(UPLOAD_FOLDER, "Enrolement_Dummy Data.xlsx"))
        df2 = pd.read_excel(os.path.join(UPLOAD_FOLDER, "4th Year Elective Allocation.xlsx"))

        # Print column names for debugging
        print("Columns in student file:", df1.columns.tolist())
        print("Columns in allocation file:", df2.columns.tolist())

        df1.columns = df1.columns.str.strip()
        df2.columns = df2.columns.str.strip()

        chosen_subjects = df1[df1["Roll No"] == roll_no]["Chosen Subjects"].values
        allocated_subjects = df2[df2["Roll No"] == roll_no]["Allocated Subjects"].values

        return {
            "Roll No": roll_no,
            "Chosen": chosen_subjects[0] if len(chosen_subjects) > 0 else "Not Found",
            "Allocated": allocated_subjects[0] if len(allocated_subjects) > 0 else "Not Found",
            "Status": "Mismatch" if chosen_subjects != allocated_subjects else "Match"
        }
    except Exception as e:
        return {"error": str(e)}
