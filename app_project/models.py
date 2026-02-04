from extensions import db
from enum import Enum
from datetime import datetime


#---------STUDENT SYSTEM------------
class Branch(db.Model):
    __tablename__ = "branch"
    branch_id = db.Column(db.Integer,primary_key = True)
    branch_name = db.Column(db.String(50), nullable=False, unique=True)

class Year(db.Model):
    __tablename__ = "year"
    year_id = db.Column(db.Integer, primary_key=True)
    year_name = db.Column(db.String(3), nullable=False)

    branch_id = db.Column(db.Integer, db.ForeignKey("branch.branch_id"), nullable=False)
    branch = db.relationship("Branch", backref="years")

    __table_args__ = (db.UniqueConstraint("year_name","branch_id"),)

class Section(db.Model):
    __tablename__ = "section"
    section_id = db.Column(db.Integer,primary_key=True)
    section_name= db.Column(db.String(3), nullable=False)

    year_id= db.Column(db.Integer, db.ForeignKey("year.year_id"), nullable=False)
    year = db.relationship("Year", backref="sections")

    __table_args__=(db.UniqueConstraint("section_name","year_id"),)

class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, primary_key=True)
    roll_no= db.Column(db.Integer, nullable=False)
    name= db.Column(db.String(30), nullable= False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        unique=True,
        nullable=True
    )

    section_id = db.Column(db.Integer, db.ForeignKey("section.section_id"), nullable=False)
    user = db.relationship("User", back_populates="student")
    section = db.relationship("Section", backref="students")
    def __repr__(self):
        return f"<Student {self.roll_no}>"
    __table_args__ = (db.UniqueConstraint("roll_no", "section_id"),)


#------------------CIRCULAR SYSTEM------------------
class Circular(db.Model):
    __tablename__ = "circular"
    circular_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    attachments = db.relationship(
        "CircularAttachment",
        back_populates="circular",
        cascade="all, delete-orphan"
    )
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class CircularTarget(db.Model):
    __tablename__ = "circular_target"
    id = db.Column(db.Integer, primary_key=True)
    circular_id = db.Column(db.Integer, db.ForeignKey("circular.circular_id"), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey("branch.branch_id"))
    year_id = db.Column(db.Integer, db.ForeignKey("year.year_id"))
    section_id = db.Column(db.Integer, db.ForeignKey("section.section_id"))

class CircularAttachment(db.Model):
    __tablename__ = "circular_attachments"
    attachment_id = db.Column(db.Integer, primary_key=True)
    circular_id = db.Column(db.Integer, db.ForeignKey("circular.circular_id"), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(20), nullable=False)

    circular = db.relationship(
        "Circular",
        back_populates="attachments"
    )
    uploaded_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class StudentCircularStatus(db.Model):
    __tablename__ = "student_circular_status"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    circular_id = db.Column(db.Integer, db.ForeignKey("circular.circular_id"), nullable=False)
    read_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    __table_args__= (db.UniqueConstraint("student_id","circular_id",name="unique_student_circular_read"),)

class UserRole(Enum):
    ADMIN = "ADMIN"
    STUDENT = "STUDENT"


class UserStatus(Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    status = db.Column(db.Enum(UserStatus), nullable=False, default=UserStatus.PENDING)
    created_at= db.Column(db.DateTime, default=datetime.utcnow)
    student = db.relationship("Student", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.email} {self.role.value}>"










