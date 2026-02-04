from flask import Blueprint,jsonify,request
from extensions import db
from models import Branch, Year, Section, Student
from middlewares.auth_middleware import required_role

student_bp = Blueprint("student",__name__)

@student_bp.route("/student/ping")
def ping():
    return {"ping": "ok"}


#api for adding branches----------------------------
@student_bp.route("/branches", methods=["POST"])
@required_role("ADMIN")
def add_branch():
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "Input should only be json"
        }),400
    branch_name = data.get("branch_name")
    if not branch_name:
        return jsonify({
            "error" : "branch_name is required"
        }),400
    branch = Branch(branch_name=data["branch_name"])
    existing = Branch.query.filter_by(branch_name=branch_name).first()
    if existing:
        return {"error": "Branch already exists"}, 409

    db.session.add(branch)
    db.session.commit()
    return jsonify({
        "message": "Branch added",
        "branch_id": branch.branch_id
    }),201


#api for viewing branches-----------------------
@student_bp.route("/branches", methods= ["GET"])
@required_role("ADMIN")
def get_branch():
    branches = Branch.query.all()
    result=[]
    for x in branches:
        result.append({
            "branch_name": x.branch_name,
            "branch_id": x.branch_id
        })
    return jsonify(result)

#api for adding years-----------------------------
@student_bp.route("/years", methods= ["POST"])
@required_role("ADMIN")

def add_year():
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "Input should be json"
        }),400
    if "year_name" not in data or "branch_id" not in data:
        return jsonify({
            "error": "year_name is required"
        }),400
    if not Branch.query.get(data["branch_id"]):
        return jsonify({
            "error": "Branch not found"
        }),404
    year_name = data.get("year_name")
    branch_id = data.get("branch_id")
    existing = Year.query.filter_by(
        year_name=year_name,
        branch_id=branch_id
    ).first()

    if existing:
        return {"error": "Year already exists for this branch"}, 409

    year= Year(year_name=data["year_name"], branch_id=data["branch_id"])
    db.session.add(year)
    db.session.commit()
    return jsonify({
        "message": "Year added",
        "year_id": year.year_id
    })

#api for viewing year-------------------------
@student_bp.route("/years", methods = ["GET"])
@required_role("ADMIN")
def get_year():
    branch_id = request.args.get("branch_id")
    if not branch_id:
        return jsonify({
            "error": "branch_id is required"
        }),400
    years = Year.query.filter_by(branch_id = branch_id).all()
    result = []
    for x in years:
        result.append({
            "year_id": x.year_id,
            "year_name": x.year_name
        })
    return jsonify(result)

#api for adding section---------------------------

@student_bp.route("/sections", methods=["POST"])
@required_role("ADMIN")
def add_sections():
    data = request.get_json()
    section_name = data.get("section_name")
    year_id = data.get("year_id")
    if not data:
        return jsonify({
            "error": "Input should be json"
        }),400
    if "section_name" not in data or "year_id" not in data:
        return jsonify({
            "error": "section_name is required"
        }),400
    if not Year.query.get(data["year_id"]):
        return jsonify({
            "error": "Year not found"
        }),404
    section = Section(section_name=data["section_name"],year_id=data["year_id"])
    existing = Section.query.filter_by(
        section_name=section_name,
        year_id=year_id
    ).first()

    if existing:
        return {"error": "Section already exists for this year"}, 409

    db.session.add(section)
    db.session.commit()
    return jsonify({
        "message": "Section added",
        "section_id": section.section_id
    }),201

#api for viewing sections-----------------------
@student_bp.route("/sections", methods=["GET"])
@required_role("ADMIN")
def get_section():
    year_id = request.args.get("year_id")
    if not year_id:
        return jsonify({
            "error": "year_id is required"
        }),400
    sections = Section.query.filter_by(year_id=year_id).all()
    result = []
    for x in sections:
        result.append({
            "section_id": x.section_id,
            "section_name": x.section_name
        })
    return jsonify(result)

#api for adding students-------------------------
@student_bp.route("/students", methods= ["POST"])
@required_role("ADMIN")
def add_student():
    data= request.get_json()
    required = {"name","roll_no","section_id"}
    if not data:
        return jsonify({
            "error": "Input should be json"
        }),400
    if not required.issubset(data):
        return jsonify({
            "error": "name, roll_no, section_id are required"
        }),400
    if not Section.query.get(data["section_id"]):
        return jsonify({
            "error": "Section not found"
        }),404
    name = data.get("name")
    roll_no = data.get("roll_no")
    section_id = data.get("section_id")
    existing = Student.query.filter_by(
        roll_no=roll_no,
        section_id=section_id
    ).first()


    if existing:
        return {"error": "Student already exists in this section"}, 409

    student = Student(name=data["name"],roll_no=data["roll_no"],section_id=data["section_id"])
    db.session.add(student)
    db.session.commit()
    return jsonify({
        "message": "student was added",
        "student_id": student.student_id
    }),201

#api for viewing student--------------------------
@student_bp.route("/students", methods=["GET"])
@required_role("ADMIN")
def get_student():
    section_id = request.args.get("section_id")
    if not section_id:
        return jsonify({
            "error": "section_id query param required"
        }),400
    students = Student.query.filter_by(section_id=section_id).all()
    result = []
    for x in students:
        result.append({
            "name": x.name,
            "roll_no": x.roll_no,
            "student_id": x.student_id
        })
    return jsonify(result)
















