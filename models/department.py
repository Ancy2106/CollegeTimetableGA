from models import db


class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)

    department_name = db.Column(
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

    academic_year = db.Column(
        db.String(20),
        nullable=False
    )

    def __repr__(self):
        return f"<Department {self.department_name}>"
