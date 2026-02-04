from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from models import db, User, UserRole, UserStatus
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


#api for signup-----------------------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email= data.get("email")
    password= data.get("password")
    if not email or not password:
        return jsonify({
            "message": "email and password are required"
        })
    existing_user= User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({
            "message": "User already exists."
        })
    user = User(email=email, password=generate_password_hash(password), role=UserRole.STUDENT, status=UserStatus.PENDING)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "Signup Successful"
    })

#api for login-----------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data= request.get_json()
    email= data.get("email")
    password= data.get("password")
    if not email or not password:
        return jsonify({
            "message": "email and password are required"
        })
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({
            "error": "Invalid credentials"
        })
    access = create_access_token(
        identity=str(user.user_id),
        additional_claims={
            "role": user.role.value,
            "status": user.status.value
        }
    )
    return jsonify({
        "access_token": access
    })




