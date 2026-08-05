from models import db


class Semester(db.Model):
    __tablename__ = "semesters"

    id = db.Column(db.Integer, primary_key=True)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id"),
        nullable=False
    )

    semester = db.Column(
        db.Integer,
        nullable=False
    )

    academic_year = db.Column(
        db.String(20),
        nullable=False
    )

    department = db.relationship(
        "Department",
        backref="semesters"
    )

    def __repr__(self):
        return f"Semester {self.semester}"
