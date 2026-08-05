from flask import Blueprint, render_template, redirect, url_for, flash

from models import db

from models.faculty import Faculty
from models.subject import Subject
from models.classroom import Classroom
from models.department import Department
from models.timeslot import TimeSlot
from models.timetable import Timetable
from models.subject_allocation import SubjectAllocation
from models.faculty_availability import FacultyAvailability

from ga.genetic_algorithm import GeneticAlgorithm


timetable_bp = Blueprint(
    "timetable",
    __name__,
    url_prefix="/timetable"
)


# =========================================================
# TIMETABLE PAGE
# =========================================================

@timetable_bp.route("/")
def timetable():

    timetables = Timetable.query.order_by(
        Timetable.department,
        Timetable.semester,
        Timetable.section,
        Timetable.day,
        Timetable.period
    ).all()

    timeslots = TimeSlot.query.order_by(
        TimeSlot.period
    ).all()

    return render_template(
        "timetable/timetable.html",
        timetables=timetables,
        timeslots=timeslots
    )
# =========================================================
# GENERATE TIMETABLE
# =========================================================


@timetable_bp.route("/generate")
def generate_timetable():

    # -----------------------------------------------------
    # LOAD DATABASE DATA
    # -----------------------------------------------------

    faculty = Faculty.query.all()

    subjects = Subject.query.all()

    classrooms = Classroom.query.all()

    departments = Department.query.all()

    timeslots = TimeSlot.query.all()

    allocations = SubjectAllocation.query.all()

    availability = FacultyAvailability.query.all()

    # -----------------------------------------------------
    # BASIC VALIDATION
    # -----------------------------------------------------

    if not allocations:

        flash(
            "No subject allocations found. "
            "Please create subject allocations first.",
            "warning"
        )

        return redirect(
            url_for("timetable.timetable")
        )

    if not timeslots:

        flash(
            "No time slots found. "
            "Please create time slots first.",
            "warning"
        )

        return redirect(
            url_for("timetable.timetable")
        )

    if not classrooms:

        flash(
            "No classrooms found. "
            "Please create classrooms first.",
            "warning"
        )

        return redirect(
            url_for("timetable.timetable")
        )

    # -----------------------------------------------------
    # CREATE GENETIC ALGORITHM
    # -----------------------------------------------------

    ga = GeneticAlgorithm(

        faculty=faculty,

        subjects=subjects,

        classrooms=classrooms,

        departments=departments,

        timeslots=timeslots,

        allocations=allocations,

        availability=availability,

        population_size=30,

        generations=100,

        mutation_rate=0.10
    )

    # -----------------------------------------------------
    # RUN GENETIC ALGORITHM
    # -----------------------------------------------------

    best_solution = ga.run()

    # -----------------------------------------------------
    # CHECK RESULT
    # -----------------------------------------------------

    if best_solution is None:

        flash(
            "Timetable generation failed.",
            "danger"
        )

        return redirect(
            url_for("timetable.timetable")
        )

    # -----------------------------------------------------
    # REMOVE OLD GENERATED TIMETABLE
    # -----------------------------------------------------

    Timetable.query.delete()

    db.session.commit()

    # -----------------------------------------------------
    # SAVE GENERATED TIMETABLE
    # -----------------------------------------------------

    for lecture in best_solution.timetable:

        timetable_entry = Timetable(

            department=lecture["department"],

            semester=int(lecture["semester"]),

            section=lecture["section"],

            subject=lecture["subject"],

            subject_type=lecture["type"],

            faculty=lecture["faculty"],

            room=lecture["room"],

            day=lecture["day"],

            period=int(lecture["period"]),

            start_time=lecture["start_time"],

            end_time=lecture["end_time"],

            session=lecture["session"],

            allocation_id=lecture["allocation_id"],

            timeslot_id=lecture["timeslot_id"]

        )

        db.session.add(
            timetable_entry
        )

    db.session.commit()

    # -----------------------------------------------------
    # SUCCESS MESSAGE
    # -----------------------------------------------------

    flash(
        f"Timetable generated successfully! "
        f"Fitness: {best_solution.fitness}",
        "success"
    )

    return redirect(
        url_for("timetable.timetable")
    )


# =========================================================
# CLEAR TIMETABLE
# =========================================================

@timetable_bp.route("/clear", methods=["POST"])
def clear_timetable():

    Timetable.query.delete()

    db.session.commit()

    flash(
        "Timetable cleared successfully.",
        "success"
    )

    return redirect(
        url_for("timetable.timetable")
    )
# =========================================================
# TIMETABLE REPORTS
# =========================================================


@timetable_bp.route("/reports")
def reports():

    timetables = Timetable.query.order_by(
        Timetable.department,
        Timetable.semester,
        Timetable.section,
        Timetable.day,
        Timetable.period
    ).all()

    timeslots = TimeSlot.query.order_by(
        TimeSlot.period
    ).all()

    timetable_map = {}

    for lecture in timetables:

        key = (
            lecture.department,
            lecture.semester,
            lecture.section
        )

        timetable_map.setdefault(key, []).append(lecture)

    return render_template(
        "timetable/reports.html",
        timetable_map=timetable_map,
        timeslots=timeslots
    )
