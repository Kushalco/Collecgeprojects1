from flask import Flask
from app.routes.admin_routes import admin_bp
import os

app = Flask(__name__)

# Set Upload Folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Register Blueprints
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
