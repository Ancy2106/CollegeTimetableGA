from models import db


class Timetable(db.Model):
    __tablename__ = "timetable"

    id = db.Column(db.Integer, primary_key=True)

    # Class Details
    department = db.Column(db.String(100), nullable=False)
    semester = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(10), nullable=False)

    # Subject Details
    subject = db.Column(db.String(100), nullable=False)
    subject_type = db.Column(db.String(20), nullable=False)

    # Faculty
    faculty = db.Column(db.String(100), nullable=False)

    # Room
    room = db.Column(db.String(50), nullable=False)

    # Day & Period
    day = db.Column(db.String(20), nullable=False)
    period = db.Column(db.Integer, nullable=False)

    # Time
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)

    # Session
    session = db.Column(
        db.String(20),
        default="Teaching"
    )

    # References
    allocation_id = db.Column(db.Integer)
    timeslot_id = db.Column(db.Integer)

    def __repr__(self):

        return (
            f"{self.department} "
            f"Sem-{self.semester} "
            f"{self.section} "
            f"{self.day} "
            f"P{self.period}"
        )
