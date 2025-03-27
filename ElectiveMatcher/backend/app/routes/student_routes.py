import os
from flask import Blueprint, jsonify
from config import UPLOAD_FOLDER
from app.services.file_service import get_student_subjects

student_bp = Blueprint("student", __name__)

@student_bp.route("/student/subjects/<roll_no>", methods=["GET"])
def get_student(roll_no):
    try:
        result = get_student_subjects(roll_no)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
