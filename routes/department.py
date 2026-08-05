from flask import Blueprint, render_template, request, redirect, url_for

from models import db
from models.department import Department
from utils.auth import login_required

department_bp = Blueprint(
    "department",
    __name__
)


@department_bp.route("/departments")
@login_required
def departments():

    department_list = Department.query.order_by(
        Department.department_name
    ).all()

    return render_template(
        "department/departments.html",
        departments=department_list
    )


@department_bp.route(
    "/departments/add",
    methods=["GET", "POST"]
)
@login_required
def add_department():

    if request.method == "POST":

        department = Department(

            department_name=request.form["department_name"],

            semester=request.form["semester"],

            section=request.form["section"],

            academic_year=request.form["academic_year"]

        )

        db.session.add(department)

        db.session.commit()

        return redirect(
            url_for("department.departments")
        )

    return render_template(
        "department/add_department.html"
    )


@department_bp.route("/departments/delete/<int:id>")
@login_required
def delete_department(id):

    department = Department.query.get_or_404(id)

    db.session.delete(department)

    db.session.commit()

    return redirect(
        url_for("department.departments")
    )
