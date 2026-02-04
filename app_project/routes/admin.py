from flask import Blueprint, request, jsonify

from models import db, User, Student, UserStatus
from middlewares.auth_middleware import required_role

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/approve-student", methods=["POST"])
@required_role("ADMIN")
def approve_student():
    data = request.get_json()

    user_id = data.get("user_id")
    student_id = data.get("student_id")

    if not user_id or not student_id:
        return jsonify({
            "message": "user_id and student_id are required"
        }), 400

    # fetch user
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # ensure user is a student
    if user.role.value != "STUDENT":
        return jsonify({"message": "User is not a student"}), 400

    # fetch student
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    # check if student already linked
    if student.user_id is not None:
        return jsonify({
            "message": "Student already linked to a user"
        }), 409


    student.user_id = user.user_id
    user.status = UserStatus.ACTIVE

    db.session.commit()

    return jsonify({
        "message": "Student approved successfully"
    }), 200
