from models import db


class Classroom(db.Model):
    __tablename__ = "classrooms"

    id = db.Column(db.Integer, primary_key=True)

    room_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    room_name = db.Column(
        db.String(100),
        nullable=False
    )

    room_type = db.Column(
        db.String(20),
        nullable=False
    )

    capacity = db.Column(
        db.Integer,
        nullable=False
    )

    building = db.Column(
        db.String(50),
        nullable=False
    )

    floor = db.Column(
        db.Integer,
        nullable=False
    )

    availability = db.Column(
        db.String(20),
        default="Available"
    )

    def __repr__(self):
        return f"<Classroom {self.room_number}>"
