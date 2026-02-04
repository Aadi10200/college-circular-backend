from app import create_app
from extensions import db
from models import User, UserRole, UserStatus
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin = User.query.filter_by(email="admin@college.edu").first()

    if not admin:
        admin = User(
            email="admin@college.edu",
            password=generate_password_hash("admin123"),
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created")
    else:
        print("ℹ️ Admin already exists")
