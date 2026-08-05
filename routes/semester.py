from flask import Blueprint, render_template, request, redirect, url_for

from models import db
from models.semester import Semester
from models.department import Department

from utils.auth import login_required

semester_bp = Blueprint(
    "semester",
    __name__
)


@semester_bp.route("/semesters")
@login_required
def semesters():

    semesters = Semester.query.all()

    return render_template(
        "semester/semesters.html",
        semesters=semesters
    )


@semester_bp.route(
    "/semesters/add",
    methods=["GET", "POST"]
)
@login_required
def add_semester():

    if request.method == "POST":

        semester = Semester(

            department_id=request.form["department"],

            semester=request.form["semester"],

            academic_year=request.form["academic_year"]

        )

        db.session.add(semester)

        db.session.commit()

        return redirect(
            url_for("semester.semesters")
        )

    departments = Department.query.all()

    return render_template(
        "semester/add_semester.html",
        departments=departments
    )


@semester_bp.route("/semesters/delete/<int:id>")
@login_required
def delete_semester(id):

    semester = Semester.query.get_or_404(id)

    db.session.delete(semester)

    db.session.commit()

    return redirect(
        url_for("semester.semesters")
    )
