import os

# Get the base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Directory for CSV files
CSV_DIR = os.path.join(BASE_DIR, "data")

# Directory for uploaded Excel files
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Secret key for Flask (used for sessions, authentication, etc.)
SECRET_KEY = "1234"  # Load from environment variable or fallback

# Ensure required directories exist
for folder in [UPLOAD_FOLDER, CSV_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

# Allowed file extensions for uploads
ALLOWED_EXTENSIONS = {"xlsx"}
