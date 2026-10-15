
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student")

    bookings = db.relationship("Booking", back_populates="user")
    examinationslots = db.relationship(
        "ExaminationSlot", back_populates="user"
    )
    profile = db.relationship(
        "ExaminerProfile", back_populates="examiner", uselist=False
    )


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True)
    c_code = db.Column(db.String(100), unique=True, nullable=False)
    c_name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(100), nullable=False)

    exams = db.relationship("Examination", back_populates="course")


class Examination(db.Model):
    __tablename__ = "examination"

    id = db.Column(db.Integer, primary_key=True)

    course_id = db.Column(
        db.Integer, db.ForeignKey("course.id"), nullable=False
    )
    ex_name = db.Column(db.String(100), nullable=False)
    
    ex_type = db.Column(
        db.String(50), nullable=False, default="Assessment"
    )
    duration = db.Column(db.Integer, nullable=False)
    max_mark = db.Column(db.Integer, nullable=False, default=100)

    slot_start = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    slot_end = db.Column(db.DateTime(timezone=True), nullable=False)

    booking_start = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    booking_end = db.Column(db.DateTime(timezone=True), nullable=False)

    status = db.Column(db.String(50), nullable=False, default="Draft")

    course = db.relationship("Course", back_populates="exams")
    rubrics = db.relationship("ExaminRubric", back_populates="exam")
    examinationslots = db.relationship(
        "ExaminationSlot", back_populates="examination"
    )


class ExaminRubric(db.Model):
    __tablename__ = "examin_rubric"

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(
        db.Integer, db.ForeignKey("examination.id"), nullable=False
    )
    criterion_name = db.Column(db.String(100), nullable=False)
    max_mark = db.Column(db.Integer, nullable=False, default=100)

    # Example: 25.50 means 25.50%
    weightage = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    description = db.Column(db.Text, nullable=False)

    exam = db.relationship("Examination", back_populates="rubrics")


class ExaminationSlot(db.Model):
    __tablename__ = "examinationslot"

    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(
        db.Integer, db.ForeignKey("examination.id"), nullable=False
    )
    examiner_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )

    date = db.Column(db.Date, nullable=False)
    start = db.Column(db.DateTime(timezone=True), nullable=False)
    end = db.Column(db.DateTime(timezone=True), nullable=False)

    max_student = db.Column(db.Integer, nullable=False)
    available_seat = db.Column(db.Integer, nullable=False)

    status = db.Column(
        db.String(100), nullable=False, default="Available"
    )

    examination = db.relationship(
        "Examination", back_populates="examinationslots"
    )
    user = db.relationship("User", back_populates="examinationslots")
    bookings = db.relationship("Booking", back_populates="exam_slot")


class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )
    slot_id = db.Column(
        db.Integer, db.ForeignKey("examinationslot.id"), nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id", "slot_id", name="uq_booking_student_slot"
        ),
    )

    user = db.relationship("User", back_populates="bookings")
    exam_slot = db.relationship(
        "ExaminationSlot", back_populates="bookings"
    )


class ExaminerProfile(db.Model):
    __tablename__ = "examiner_profile"

    # Shared primary key: one profile per user
    id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True
    )

    department = db.Column(db.Text)
    status = db.Column(db.String(100))

    examiner = db.relationship("User", back_populates="profile")