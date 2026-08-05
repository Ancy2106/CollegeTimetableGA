from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from models import db
from models.faculty import Faculty
from utils.auth import login_required


faculty_bp = Blueprint(
    "faculty",
    __name__
)


@faculty_bp.route("/faculty")
@login_required
def faculty_home():

    faculty = Faculty.query.order_by(
        Faculty.id.desc()
    ).all()

    return render_template(
        "faculty/faculty.html",
        faculty=faculty
    )


@faculty_bp.route("/faculty/add", methods=["GET", "POST"])
@login_required
def add_faculty():

    if request.method == "POST":

        new_faculty = Faculty(

            faculty_name=request.form["faculty_name"],

            faculty_code=request.form["faculty_code"],

            department=request.form["department"],

            designation=request.form["designation"],

            email=request.form["email"],

            phone=request.form["phone"],

            availability=request.form["availability"]

        )

        db.session.add(new_faculty)

        db.session.commit()

        return redirect(
            url_for("faculty.faculty_home")
        )

    return render_template(
        "faculty/add_faculty.html"
    )


@faculty_bp.route("/faculty/delete/<int:id>")
@login_required
def delete_faculty(id):

    faculty = Faculty.query.get_or_404(id)

    db.session.delete(faculty)

    db.session.commit()

    return redirect(
        url_for("faculty.faculty_home")
    )
