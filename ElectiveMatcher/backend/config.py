import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

CSV_DIR = os.path.join(BASE_DIR, "data")

SECRET_KEY = "1234"

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)
