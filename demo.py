import pandas as pd
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from fpdf import FPDF  # Library to create PDFs

# Function to clean subject strings (remove spaces and special characters)
def clean_subject(subject):
    return re.sub(r'\W+', '', subject)

# Function to process a DataFrame and extract cleaned subjects
def process_subjects(df, subject_columns):
    df['Chosen Subjects'] = df.apply(
        lambda row: ','.join([
            clean_subject(row[col]) for col in subject_columns if pd.notna(row[col])
        ]),
        axis=1
    )
    return df

# Function to dynamically identify the roll number column
def identify_roll_no_column(df):
    roll_no_keywords = ['roll', 'univ', 'university', 'rollno', 'univrollno', 'universityrollno']
    for col in df.columns:
        if any(keyword in col.lower() for keyword in roll_no_keywords):
            return col
    return None

# Function to dynamically identify the name column
def identify_name_column(df):
    name_keywords = ['name', 'student', 'studentname', 'studentsname']
    for col in df.columns:
        if any(keyword in col.lower() for keyword in name_keywords):
            return col
    return None

# Function to remove unusual words from subjects
def remove_unusual_words(subjects, unusual_words):
    for word in unusual_words:
        subjects = subjects.replace(word, '')
    return subjects

# Function to compare subjects from two dataframes
def compare_subjects(df1, df2, roll_no_col1, roll_no_col2, unusual_words):
    comparison_results = []
    for index, row in df1.iterrows():
        roll_no = row[roll_no_col1]
        subjects1 = row['Chosen Subjects']
        subjects2 = df2[df2[roll_no_col2] == roll_no]['Chosen Subjects'].values
        if subjects2:
            subjects2 = remove_unusual_words(subjects2[0], unusual_words)
            if clean_subject(subjects1) == clean_subject(subjects2):
                comparison_results.append((roll_no, subjects1, subjects2, 'Match'))
            else:
                comparison_results.append((roll_no, subjects1, subjects2, 'Mismatch'))
        else:
            comparison_results.append((roll_no, subjects1, 'Not Found', 'Not Found'))
    return comparison_results

# Function to process and compare subjects from two files
def process_and_compare(file1, file2, subject_columns_file1, subject_columns_file2, unusual_words):
    try:
        elective_allocation = pd.read_excel(file1, sheet_name='Sheet1')
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}. Please check the file path.")

    elective_allocation.columns = elective_allocation.columns.str.strip()
    roll_no_col_file1 = identify_roll_no_column(elective_allocation)
    if roll_no_col_file1 is None:
        raise KeyError("Roll number column not found in the first file.")

    name_col_file1 = identify_name_column(elective_allocation)
    if name_col_file1 is None:
        raise KeyError("Name column not found in the first file.")

    elective_allocation = elective_allocation.dropna(subset=[roll_no_col_file1])
    elective_allocation = process_subjects(elective_allocation, subject_columns_file1)

    try:
        enrollment_data = pd.read_excel(file2, sheet_name='Sheet1')
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}. Please check the file path.")

    enrollment_data.columns = enrollment_data.columns.str.strip()
    roll_no_col_file2 = identify_roll_no_column(enrollment_data)
    if roll_no_col_file2 is None:
        raise KeyError("Roll number column not found in the second file.")

    name_col_file2 = identify_name_column(enrollment_data)
    if name_col_file2 is None:
        raise KeyError("Name column not found in the second file.")

    enrollment_data = enrollment_data.dropna(subset=[roll_no_col_file2])
    enrollment_data = process_subjects(enrollment_data, subject_columns_file2)

    comparison_results = compare_subjects(elective_allocation, enrollment_data, roll_no_col_file1, roll_no_col_file2, unusual_words)
    return comparison_results

# Function to handle the file selection and comparison
def compare_files():
    file1 = file1_entry.get()
    file2 = file2_entry.get()
    
    if not file1 or not file2:
        messagebox.showerror("Error", "Please select both files.")
        return
    
    subject_columns_file1 = [
        'Professional Elective VI', 'Unnamed: 4', 'Open Elective III', 
        'Unnamed: 6', 'Open Elective IV', 'Unnamed: 8'
    ]
    subject_columns_file2 = ['Subjects']
    unusual_words = ['PCCCS601', 'PCCCS602', 'PROJCS601', 'PCCCS691', 'PCCCS692']
    
    try:
        global comparison_results
        comparison_results = process_and_compare(file1, file2, subject_columns_file1, subject_columns_file2, unusual_words)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "\nComparison of chosen subjects:\n")
        for result in comparison_results:
            result_text.insert(tk.END, f"Roll No.: {result[0]}, File 1 Subjects: {result[1]}, File 2 Subjects: {result[2]}, Result: {result[3]}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to export results to PDF
def export_to_pdf():
    if not comparison_results:
        messagebox.showerror("Error", "No results to export.")
        return
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)  # Reduced font size
    
    # Title
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 255)  # Blue color for title
    pdf.cell(200, 10, txt="Subject Comparison Results", ln=True, align='C')
    pdf.ln(10)
    
    # Table Header
    pdf.set_font("Arial", 'B', 10)
    pdf.set_text_color(0, 0, 0)  # Black color for header
    pdf.set_fill_color(200, 220, 255)  # Light blue background for header
    pdf.cell(40, 10, txt="Roll No.", border=1, align='C', fill=True)
    pdf.cell(70, 10, txt="File 1 Subjects", border=1, align='C', fill=True)
    pdf.cell(70, 10, txt="File 2 Subjects", border=1, align='C', fill=True)
    pdf.cell(20, 10, txt="Result", border=1, align='C', fill=True, ln=True)
    
    # Table Rows
    pdf.set_font("Arial", size=10)
    for result in comparison_results:
        pdf.set_text_color(0, 0, 0)  # Black color for text
        pdf.cell(40, 10, txt=str(result[0]), border=1)
        pdf.cell(70, 10, txt=result[1], border=1)
        pdf.cell(70, 10, txt=result[2], border=1)
        if result[3] == 'Match':
            pdf.set_text_color(0, 128, 0)  # Green color for 'Match'
        elif result[3] == 'Mismatch':
            pdf.set_text_color(255, 0, 0)  # Red color for 'Mismatch'
        else:
            pdf.set_text_color(0, 0, 0)  # Black color for 'Not Found'
        pdf.cell(20, 10, txt=result[3], border=1, ln=True)
    
    # Save PDF
    pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if pdf_file:
        pdf.output(pdf_file)
        messagebox.showinfo("Success", "Results exported to PDF successfully.")

# Function to open file dialog and set file path to entry
def browse_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)

# Create the main window
# Create main window
root = tk.Tk()
root.title("Subject Comparison and Verification Tool")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

# Create and place the widgets
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# File 1 Section
file1_frame = ttk.Frame(main_frame)
file1_frame.pack(fill=tk.X, pady=10)

ttk.Label(file1_frame, text="Elective Allocation File:").pack(side=tk.LEFT, padx=5)
file1_entry = ttk.Entry(file1_frame, width=50)
file1_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(file1_frame, text="Browse", command=lambda: browse_file(file1_entry)).pack(side=tk.LEFT, padx=5)

# File 2 Section
file2_frame = ttk.Frame(main_frame)
file2_frame.pack(fill=tk.X, pady=10)

ttk.Label(file2_frame, text="Enrollment Dummy Data File:").pack(side=tk.LEFT, padx=5)
file2_entry = ttk.Entry(file2_frame, width=50)
file2_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(file2_frame, text="Browse", command=lambda: browse_file(file2_entry)).pack(side=tk.LEFT, padx=5)

# Compare Button
compare_button = ttk.Button(main_frame, text="Compare Files", command=compare_files)
compare_button.pack(pady=15)

# Export to PDF Button
export_button = ttk.Button(main_frame, text="Export Results to PDF", command=export_to_pdf)
export_button.pack(pady=10)

# Result Section
result_frame = ttk.Frame(main_frame)
result_frame.pack(fill=tk.BOTH, expand=True)

result_text = scrolledtext.ScrolledText(result_frame, width=100, height=20, font=('Arial', 11))
result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)

# Run the application
root.mainloop()