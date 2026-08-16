from models import db


class Subject(db.Model):

    __tablename__ = "subjects"

    __table_args__ = (

        db.UniqueConstraint(
            "subject_code",
            "semester",
            "department_id",
            "section",
            name="uq_subject_code_semester_department_section"
        ),

    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    subject_code = db.Column(
        db.String(20),
        nullable=False
    )

    subject_name = db.Column(
        db.String(100),
        nullable=False
    )

    semester = db.Column(
        db.Integer,
        nullable=False
    )

    section = db.Column(
        db.String(10),
        nullable=False
    )

    hours_per_week = db.Column(
        db.Integer,
        nullable=False
    )

    subject_type = db.Column(
        db.String(20),
        nullable=False
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculty.id"),
        nullable=False
    )

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    faculty = db.relationship(
        "Faculty",
        backref="subjects"
    )

    department = db.relationship(
        "Department",
        backref="subjects"
    )

    def __repr__(self):

        return (
            f"<Subject "
            f"{self.subject_code} - "
            f"{self.subject_name} - "
            f"Sem {self.semester} - "
            f"Section {self.section}>"
        )
