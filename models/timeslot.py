from models import db


class TimeSlot(db.Model):
    __tablename__ = "timeslots"

    id = db.Column(db.Integer, primary_key=True)

    day = db.Column(
        db.String(20),
        nullable=False
    )

    period = db.Column(
        db.Integer,
        nullable=False
    )

    start_time = db.Column(
        db.String(10),
        nullable=False
    )

    end_time = db.Column(
        db.String(10),
        nullable=False
    )

    session = db.Column(
        db.String(20),
        nullable=False
    )

    def __repr__(self):
        return f"{self.day} P{self.period}"
