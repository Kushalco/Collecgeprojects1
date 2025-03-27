import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from config import UPLOAD_FOLDER
from file_services import process_and_compare

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/upload", methods=["POST"])
def upload_files():
    try:
        if "file1" not in request.files or "file2" not in request.files:
            return jsonify({"error": "Both files must be uploaded"}), 400

        file1 = request.files["file1"]
        file2 = request.files["file2"]

        if file1.filename == "" or file2.filename == "":
            return jsonify({"error": "No file selected"}), 400

        # Save uploaded files
        file1_path = os.path.join(UPLOAD_FOLDER, secure_filename(file1.filename))
        file2_path = os.path.join(UPLOAD_FOLDER, secure_filename(file2.filename))
        file1.save(file1_path)
        file2.save(file2_path)

        return jsonify({"message": "Files uploaded successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route("/admin/mismatches", methods=["GET"])
def get_mismatches():
    try:
        file1_path = os.path.join(UPLOAD_FOLDER, "Enrolement_Dummy Data.xlsx")
        file2_path = os.path.join(UPLOAD_FOLDER, "4th Year Elective Allocation.xlsx")

        if not os.path.exists(file1_path) or not os.path.exists(file2_path):
            return jsonify({"error": "Files not found"}), 404

        mismatches = process_and_compare(file1_path, file2_path)
        return jsonify(mismatches), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
