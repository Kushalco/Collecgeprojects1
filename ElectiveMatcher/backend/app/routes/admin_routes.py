from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER
from app.services.file_service import process_and_compare

admin_bp = Blueprint("admin", __name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"xlsx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route("/admin/upload", methods=["POST"])
def upload_files():
    if "file1" not in request.files or "file2" not in request.files:
        return jsonify({"error": "Missing files"}), 400

    file1 = request.files["file1"]
    file2 = request.files["file2"]

    if file1.filename == "" or file2.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)

        filepath1 = os.path.join(UPLOAD_FOLDER, filename1)
        filepath2 = os.path.join(UPLOAD_FOLDER, filename2)

        print(f"Saving file1 at: {filepath1}")  # Debugging log
        print(f"Saving file2 at: {filepath2}")  # Debugging log

        file1.save(filepath1)
        file2.save(filepath2)

        return jsonify({
            "message": "Files uploaded successfully",
            "file1": filename1,
            "file2": filename2
        }), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

# 📌 **2️⃣ Admin Mismatch API**
@admin_bp.route("/admin/mismatches", methods=["GET"])
def get_mismatches():
    file1 = "Enrolement_Dummy Data.xlsx"
    file2 = "4th Year Elective Allocation.xlsx"

    file1_path = os.path.join(UPLOAD_FOLDER, file1)
    file2_path = os.path.join(UPLOAD_FOLDER, file2)

    print(f"checking file1: {file1_path}")
    print(f"checking file2: {file2_path}")

    # Ensure files are uploaded first
    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        return jsonify({"error": "Files not found. Please upload first!"}), 400

    mismatches = process_and_compare(file1_path, file2_path)
    
    return jsonify({"mismatches": mismatches}), 200
