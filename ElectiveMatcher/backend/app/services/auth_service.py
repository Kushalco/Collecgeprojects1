import csv
import os
from werkzeug.security import generate_password_hash, check_password_hash
from config import CSV_DIR

STUDENT_CSV = os.path.join(CSV_DIR, "students.csv")

def register_student(data):
    roll_no = data.get("roll_no")
    name = data.get("name")
    password = data.get("password")

    if not (roll_no and name and password):
        return {"error": "All fields are required"}, 400

    hashed_password = generate_password_hash(password)

    with open(STUDENT_CSV, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([roll_no, name, hashed_password])
    
    return {"message": "Student registered successfully"}, 201

def login_student(data):
    roll_no = data.get("roll_no")
    password = data.get("password")

    with open(STUDENT_CSV, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == roll_no and check_password_hash(row[2], password):
                return {"message": "Login successful"}, 200
    
    return {"error": "Invalid credentials"}, 401
