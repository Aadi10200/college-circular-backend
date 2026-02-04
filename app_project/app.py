from flask import Flask
from extensions import db, jwt
import os

def create_app():
    app = Flask(__name__)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "data.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "super-secret-key"

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



    with app.app_context():
        db.create_all()

    return app


# Create the app
app = create_app()

# Run the server
if __name__ == "__main__":
    app.run(debug=True)
