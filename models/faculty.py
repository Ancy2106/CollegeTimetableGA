from models import db


class Faculty(db.Model):
    __tablename__ = "faculty"

    id = db.Column(db.Integer, primary_key=True)

    faculty_name = db.Column(
        db.String(100),
        nullable=False
    )

    faculty_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    designation = db.Column(
        db.String(50),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    phone = db.Column(
        db.String(15),
        nullable=False
    )

    availability = db.Column(
        db.String(50),
        default="Full Time"
    )

    def __repr__(self):
        return f"<Faculty {self.faculty_name}>"
