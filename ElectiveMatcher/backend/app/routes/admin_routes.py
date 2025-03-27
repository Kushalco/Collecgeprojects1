from flask import Blueprint, request, jsonify
from app.services.file_service import process_and_compare
from app.services.search_service import search_mismatches

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/upload", methods=["POST"])
def upload_files():
    file1 = request.files.get("file1")
    file2 = request.files.get("file2")

    if not file1 or not file2:
        return jsonify({"error": "Both files are required"}), 400
    
    mismatches = process_and_compare(file1, file2)
    return jsonify(mismatches)

@admin_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("query", "")
    results = search_mismatches(query)
    return jsonify(results)
