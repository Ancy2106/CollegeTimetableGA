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

    subject_list = Subject.query.all()

    return render_template(
        "subject/subjects.html",
        subjects=subject_list
    )


@subject_bp.route("/subjects/add", methods=["GET", "POST"])
@login_required
def add_subject():

    faculty = Faculty.query.all()
    departments = Department.query.all()

    if request.method == "POST":

        subject = Subject(

            subject_code=request.form["subject_code"],

            subject_name=request.form["subject_name"],

            semester=request.form["semester"],

            hours_per_week=request.form["hours_per_week"],

            subject_type=request.form["subject_type"],

            faculty_id=request.form["faculty_id"],

            department_id=request.form["department_id"]

        )

        db.session.add(subject)

        db.session.commit()

        return redirect(url_for("subject.subjects"))

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
