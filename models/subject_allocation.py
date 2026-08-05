from models import db


class SubjectAllocation(db.Model):
    __tablename__ = "subject_allocations"

    id = db.Column(db.Integer, primary_key=True)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    semester_id = db.Column(
        db.Integer,
        db.ForeignKey("semesters.id"),
        nullable=False
    )

    section_id = db.Column(
        db.Integer,
        db.ForeignKey("sections.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculty.id"),
        nullable=False
    )

    weekly_hours = db.Column(
        db.Integer,
        nullable=False
    )

    subject_type = db.Column(
        db.String(20),
        nullable=False
    )

    consecutive_hours = db.Column(
        db.Integer,
        default=1
    )

    preferred_room = db.Column(
        db.String(20),
        nullable=False
    )

    priority = db.Column(
        db.String(20),
        default="Medium"
    )

    department = db.relationship("Department")
    semester = db.relationship("Semester")
    section = db.relationship("Section")
    subject = db.relationship("Subject")
    faculty = db.relationship("Faculty")
