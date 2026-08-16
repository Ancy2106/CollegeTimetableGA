from models import db


class Timetable(db.Model):

    __tablename__ = "timetable"

    # =====================================================
    # PRIMARY KEY
    # =====================================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # =====================================================
    # DEPARTMENT
    # =====================================================

    department = db.Column(
        db.String(100),
        nullable=False
    )

    # =====================================================
    # SEMESTER
    # =====================================================

    semester = db.Column(
        db.Integer,
        nullable=False
    )

    # =====================================================
    # SECTION
    # =====================================================

    section = db.Column(
        db.String(20),
        nullable=False
    )

    # =====================================================
    # SUBJECT
    # =====================================================

    subject = db.Column(
        db.String(150),
        nullable=False
    )

    subject_type = db.Column(
        db.String(30),
        nullable=False
    )

    # =====================================================
    # FACULTY
    # =====================================================

    faculty = db.Column(
        db.String(150),
        nullable=False
    )

    # =====================================================
    # CLASSROOM
    # =====================================================

    room = db.Column(
        db.String(50),
        nullable=False
    )

    # =====================================================
    # DAY & PERIOD
    # =====================================================

    day = db.Column(
        db.String(20),
        nullable=False
    )

    period = db.Column(
        db.Integer,
        nullable=False
    )

    # =====================================================
    # TIME
    # =====================================================

    start_time = db.Column(
        db.String(20),
        nullable=False
    )

    end_time = db.Column(
        db.String(20),
        nullable=False
    )

    session = db.Column(
        db.String(30),
        nullable=False
    )

    # =====================================================
    # REFERENCES
    # =====================================================

    allocation_id = db.Column(
        db.Integer,
        nullable=False
    )

    timeslot_id = db.Column(
        db.Integer,
        nullable=False
    )

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================

    def __repr__(self):

        return (
            f"<Timetable "
            f"{self.department} "
            f"Sem-{self.semester} "
            f"{self.section} "
            f"{self.day} "
            f"P{self.period}>"
        )
