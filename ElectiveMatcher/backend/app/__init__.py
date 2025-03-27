from flask import Flask
from config import UPLOAD_FOLDER, SECRET_KEY
from app.routes import register_routes
from app.routes.admin_routes import *;

def create_app():
    app = Flask(__name__)

    app.register_blueprint(admin_bp)

    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["SECRET_KEY"] = SECRET_KEY

    register_routes(app)

    return app