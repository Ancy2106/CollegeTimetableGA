from models import db


class Section(db.Model):
    __tablename__ = "sections"

    id = db.Column(db.Integer, primary_key=True)

    semester_id = db.Column(
        db.Integer,
        db.ForeignKey("semesters.id"),
        nullable=False
    )

    section_name = db.Column(
        db.String(10),
        nullable=False
    )

    strength = db.Column(
        db.Integer,
        nullable=False
    )

    semester = db.relationship(
        "Semester",
        backref="section_list"
    )

    def __repr__(self):
        return self.section_name
