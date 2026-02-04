from flask import Flask
from extensions import db, jwt
import os


def create_app():
    app = Flask(__name__)

    # Database (Render / Production)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    jwt.init_app(app)

    from routes.student import student_bp
    from routes.circular import circular_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp

    app.register_blueprint(student_bp)
    app.register_blueprint(circular_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
