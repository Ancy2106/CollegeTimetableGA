from models import db


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)

    subject_code = db.Column(
        db.String(20),
        unique=True,
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

    faculty = db.relationship("Faculty", backref="subjects")
    department = db.relationship("Department", backref="subjects")

    def __repr__(self):
        return f"<Subject {self.subject_name}>"
