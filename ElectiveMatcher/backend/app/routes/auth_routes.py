from flask import Blueprint, request, jsonify
from app.services.auth_service import register_student, login_student

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    return register_student(data)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    return login_student(data)
