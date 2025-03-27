from app.routes.admin_routes import admin_bp
from app.routes.student_routes import student_bp
from app.routes.auth_routes import auth_bp

def register_routes(app):
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(auth_bp, url_prefix="/auth")
