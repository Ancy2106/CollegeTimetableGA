from flask import Blueprint, render_template, request, redirect, url_for

from models import db
from models.subject import Subject
from models.faculty import Faculty
from models.department import Department
from utils.auth import login_required

subject_bp = Blueprint("subject", __name__)


@subject_bp.route("/subjects")
@login_required
def subjects():

    subjects = Subject.query.order_by(
        Subject.semester,
        Subject.section,
        Subject.subject_name
    ).all()

    departments = Department.query.order_by(
        Department.department_name
    ).all()

    faculties = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()

    return render_template(
        "subject/subjects.html",
        subjects=subjects,
        departments=departments,
        faculties=faculties
    )


@subject_bp.route(
    "/subjects/add",
    methods=["GET", "POST"]
)
@login_required
def add_subject():

    faculty = Faculty.query.all()

    departments = Department.query.all()

    if request.method == "POST":

        department_id = int(
            request.form["department_id"]
        )

        department = Department.query.get_or_404(
            department_id
        )

        subject = Subject(

            subject_code=request.form[
                "subject_code"
            ].strip(),

            subject_name=request.form[
                "subject_name"
            ].strip(),

            semester=int(
                request.form["semester"]
            ),

            # Get section from selected Department
            section=department.section,

            hours_per_week=int(
                request.form["hours_per_week"]
            ),

            subject_type=request.form[
                "subject_type"
            ].strip(),

            faculty_id=int(
                request.form["faculty_id"]
            ),

            department_id=department_id

        )

        db.session.add(subject)

        db.session.commit()

        return redirect(
            url_for("subject.subjects")
        )

    return render_template(
        "subject/add_subject.html",
        faculty=faculty,
        departments=departments
    )


@subject_bp.route("/subjects/delete/<int:id>")
@login_required
def delete_subject(id):

    subject = Subject.query.get_or_404(id)

    db.session.delete(subject)

    db.session.commit()

    return redirect(url_for("subject.subjects"))
