from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from models import UserRole, UserStatus

#middle ware to check for the logged in users----------------
def require_auth(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper

#middleware to check for the admin/ anyone else--------------------------
def required_role(required_role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != required_role:
                return jsonify({"message": "Forbidden"})
            return fn(*args, **kwargs)
        return wrapper
    return decorator

#middleware for checking students and active status------------------
def require_active_students(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()

        if claims.get("role") != UserRole.STUDENT.value:
            return jsonify({"message": "Student access only"}), 403

        if claims.get("status") != UserStatus.ACTIVE.value:
            return jsonify({"message": "Account not approved"}), 403

        return fn(*args, **kwargs)
    return wrapper