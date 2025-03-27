from flask import Blueprint, request, jsonify
from app.services.file_service import get_student_subjects

student_bp = Blueprint("student", __name__)

@student_bp.route("/mismatches", methods=["GET"])
def view_mismatches():
    roll_no = request.args.get("roll_no")
    if not roll_no:
        return jsonify({"error": "Roll number required"}), 400

    data = get_student_subjects(roll_no)
    return jsonify(data)
