import pandas as pd
import os
from config import UPLOAD_FOLDER

def process_and_compare(file1, file2):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # **Print column names for debugging**
    print("📌 Columns in Enrollment file:", df1.columns.tolist())
    print("📌 Columns in Allocation file:", df2.columns.tolist())

    # **Trim spaces from column names**
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    required_columns = {"Roll No", "Chosen Subjects", "Allocated Subjects"}

    # **Check if required columns exist**
    if not required_columns.issubset(set(df1.columns).union(set(df2.columns))):
        print("❌ Required columns missing!")
        return []

    mismatches = []
    for _, row in df1.iterrows():
        roll_no = row.get("Roll No", None)
        if roll_no is None:
            continue

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

    print(f"✅ Total mismatches found: {len(mismatches)}")
    return mismatches


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
