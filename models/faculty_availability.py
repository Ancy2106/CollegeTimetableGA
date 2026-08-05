from models import db


class FacultyAvailability(db.Model):
    __tablename__ = "faculty_availability"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    faculty_id = db.Column(
        db.Integer,
        db.ForeignKey("faculty.id"),
        nullable=False
    )

    timeslot_id = db.Column(
        db.Integer,
        db.ForeignKey("timeslots.id"),
        nullable=False
    )

    available = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    faculty = db.relationship(
        "Faculty",
        backref="availability_records"
    )

    timeslot = db.relationship(
        "TimeSlot",
        backref="faculty_records"
    )

    def __repr__(self):
        status = "Available" if self.available else "Unavailable"

        return (
            f"{self.faculty.faculty_name} - "
            f"{self.timeslot.day} "
            f"P{self.timeslot.period} - "
            f"{status}"
        )
