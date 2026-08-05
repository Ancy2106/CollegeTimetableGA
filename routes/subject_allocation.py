from flask import jsonify
from flask import Blueprint, render_template, request, redirect, url_for

from models import db

from models.department import Department
from models.semester import Semester
from models.section import Section
from models.subject import Subject
from models.faculty import Faculty
from models.subject_allocation import SubjectAllocation

from utils.auth import login_required

allocation_bp = Blueprint(
    "allocation",
    __name__
)


@allocation_bp.route("/allocations")
@login_required
def allocations():

    allocations = SubjectAllocation.query.all()

    return render_template(
        "allocation/allocations.html",
        allocations=allocations
    )


@allocation_bp.route(
    "/allocations/add",
    methods=["GET", "POST"]
)
@login_required
def add_allocation():

    if request.method == "POST":

        allocation = SubjectAllocation(

            department_id=request.form["department"],

            semester_id=request.form["semester"],

            section_id=request.form["section"],

            subject_id=request.form["subject"],

            faculty_id=request.form["faculty"],

            weekly_hours=request.form["weekly_hours"],

            subject_type=request.form["subject_type"],

            consecutive_hours=request.form["consecutive_hours"],

            preferred_room=request.form["preferred_room"],

            priority=request.form["priority"]

        )

        db.session.add(allocation)

        db.session.commit()

        return redirect(
            url_for("allocation.allocations")
        )

    return render_template(

        "allocation/add_allocation.html",

        departments=Department.query.all(),

        semesters=Semester.query.all(),

        sections=Section.query.all(),

        subjects=Subject.query.all(),

        faculty=Faculty.query.all()

    )


@allocation_bp.route("/allocations/delete/<int:id>")
@login_required
def delete_allocation(id):

    allocation = SubjectAllocation.query.get_or_404(id)

    db.session.delete(allocation)

    db.session.commit()

    return redirect(
        url_for("allocation.allocations")
    )


@allocation_bp.route("/api/semesters/<int:department_id>")
@login_required
def get_semesters(department_id):

    semesters = Semester.query.filter_by(
        department_id=department_id
    ).all()

    return jsonify([
        {
            "id": s.id,
            "semester": s.semester
        }
        for s in semesters
    ])


@allocation_bp.route("/api/sections/<int:semester_id>")
@login_required
def get_sections(semester_id):

    sections = Section.query.filter_by(
        semester_id=semester_id
    ).all()

    return jsonify([
        {
            "id": s.id,
            "name": s.section_name
        }
        for s in sections
    ])


@allocation_bp.route("/api/subjects/<int:department_id>")
@login_required
def get_subjects(department_id):

    subjects = Subject.query.filter_by(
        department_id=department_id
    ).all()

    return jsonify([
        {
            "id": s.id,
            "name": s.subject_name
        }
        for s in subjects
    ])
