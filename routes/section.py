from flask import Blueprint, render_template, request, redirect, url_for

from models import db
from models.section import Section
from models.semester import Semester

from utils.auth import login_required

section_bp = Blueprint(
    "section",
    __name__
)


@section_bp.route("/sections")
@login_required
def sections():

    sections = Section.query.all()

    return render_template(
        "section/sections.html",
        sections=sections
    )


@section_bp.route(
    "/sections/add",
    methods=["GET", "POST"]
)
@login_required
def add_section():

    if request.method == "POST":

        section = Section(

            semester_id=request.form["semester"],

            section_name=request.form["section_name"],

            strength=request.form["strength"]

        )

        db.session.add(section)

        db.session.commit()

        return redirect(
            url_for("section.sections")
        )

    semesters = Semester.query.all()

    return render_template(
        "section/add_section.html",
        semesters=semesters
    )


@section_bp.route("/sections/delete/<int:id>")
@login_required
def delete_section(id):

    section = Section.query.get_or_404(id)

    db.session.delete(section)

    db.session.commit()

    return redirect(
        url_for("section.sections")
    )
