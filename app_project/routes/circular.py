import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from extensions import db
from models import Student,Circular, CircularTarget, db,StudentCircularStatus, CircularAttachment
from routes.student import student_bp
from middlewares.auth_middleware import required_role, require_active_students
circular_bp = Blueprint("circular", __name__)

#api for adding circular------------------------
@circular_bp.route("/circular",methods = ["POST"])
@required_role("ADMIN")
def create_circular():
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "Input should be json"
        })
    if "title" not in data:
        return jsonify({
            "error": "Title is required"
        })
    circular = Circular(title=data["title"],content=data.get("content"))
    db.session.add(circular)
    db.session.commit()
    return jsonify({
        "message": "Circular created",
        "circular_id": circular.circular_id
    })

#api for circular_targeting--------------------------
@circular_bp.route("/circular/<int:circular_id>/targets", methods = ["POST"])
@required_role("ADMIN")
def add_circular_target(circular_id):
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "Input should be json"
        })
    if "targets" not in data:
        return jsonify({
            "error": "targets is required"
        })
    targets = data["targets"]
    if not isinstance(targets, list) or len(targets) == 0:
        return jsonify({"error": "targets must be a non-empty list"})
    circular = Circular.query.get(circular_id)
    if not circular:
        return jsonify({
            "error": "Circular not found"
        })
    created = 0
    for x in targets:
        valid = False
        if "branch_id" in x:
            valid = True
        if "year_id" in x:
            valid = True
        if "section_id" in x:
            valid = True
        if not valid:
            continue

        target = CircularTarget(circular_id=circular_id, branch_id=x.get("branch_id"), year_id=x.get("year_id"), section_id=x.get("section_id"))
        db.session.add(target)
        created +=1
    if created == 0:
        return jsonify({
            "error": "No valid target"
        })
    db.session.commit()
    return jsonify({
        "message": "target has been added successfully",
        "target_counts": created
    })

#api for fetching circular-------------------
@circular_bp.route("/student/<int:student_id>/circulars", methods=["GET"])
@require_active_students
def get_circulars_for_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({
            "error": "Student not found"
        })
    section_id = student.section_id
    branch_id = student.section.year.branch_id
    year_id = student.section.year_id
    targets = CircularTarget.query.filter(
        (CircularTarget.branch_id == None) | (CircularTarget.branch_id == branch_id),
        (CircularTarget.year_id == None) | (CircularTarget.year_id == year_id),
        (CircularTarget.section_id == None) | (CircularTarget.section_id == section_id)
    ).all()
    circular_ids = set()
    for x in targets:
        circular_ids.add(x.circular_id)
    circulars = Circular.query.filter(
        Circular.circular_id.in_(circular_ids)
    ).order_by(Circular.created_at.desc()).all()
    read_rows = StudentCircularStatus.query.filter_by(student_id=student_id).all()
    read_circular_ids= {row.circular_id for row in read_rows}

    result = []
    for c in circulars:
        result.append({
            "circular_id": c.circular_id,
            "title": c.title,
            "content": c.content,
            "created_at": c.created_at,
            "is_read": c.circular_id in read_circular_ids,
            "attachments": [
                {
                    "file_name": a.file_name,
                    "file_path": a.file_path,
                    "file_type": a.file_type
                }
                for a in c.attachments
            ]
        })
    return jsonify(result)

#api for adding circular read/unread status
@student_bp.route("/student/<int:student_id>/circular/<int:circular_id>/read",methods=["POST"])
def mark_circular_read(student_id,circular_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({
            "error": "Student not found"
        })
    circular = Circular.query.get(circular_id)
    if not circular:
        return jsonify({
            "error": "Circular not found"
        })
    already_read = StudentCircularStatus.query.filter_by(student_id=student_id,circular_id=circular_id).first()
    if already_read:
        return jsonify({
            "message": "Already marked as read"
        })
    status = StudentCircularStatus(student_id=student_id,circular_id=circular_id)
    db.session.add(status)
    db.session.commit()
    return {"message": "Circular marked as read"}

#api for circular attachments-----------------------------------
allowed_extensions = {"pdf","png","jpg","jpeg"}
def allowed_file(filename):
    if "." not in filename:
        return False
    if filename.rsplit(".",1)[1].lower() in allowed_extensions:
        return True
    else:
        return False
@circular_bp.route("/circular/<int:circular_id>/attachments", methods = ["POST"])
@required_role("ADMIN")
def upload_attachments(circular_id):
    circular = Circular.query.get(circular_id)
    files = request.files.getlist("files")
    if not circular:
        return jsonify({
            "error": "circular not found"
        })
    if "files" not in request.files:
        return {"error": "No files provided"}
    upload_dir = os.path.join("uploads", "circulars", str(circular_id))
    os.makedirs(upload_dir, exist_ok=True)
    for file in files:
        if file.filename == "":
            continue
        if not allowed_file(file.filename):
            return jsonify({
                "error": "Invalid file type"
            })
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        attachment = CircularAttachment(
            circular_id=circular_id,
            file_name=filename,
            file_path=file_path,
            file_type=file.content_type
        )
        db.session.add(attachment)
    db.session.commit()
    return jsonify({
        "message": "Attachments uploaded successfully"
    })























