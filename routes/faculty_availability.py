from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from models import db

from models.faculty import Faculty
from models.timeslot import TimeSlot
from models.faculty_availability import FacultyAvailability

from utils.auth import login_required


availability_bp = Blueprint(
    "availability",
    __name__
)


# ---------------------------------------------------------
# VIEW ALL FACULTY AVAILABILITY
# ---------------------------------------------------------

@availability_bp.route("/availability")
@login_required
def availability():

    records = FacultyAvailability.query.all()

    return render_template(
        "faculty_availability/availability.html",
        records=records
    )


# ---------------------------------------------------------
# ADD FACULTY AVAILABILITY
# ---------------------------------------------------------

@availability_bp.route(
    "/availability/add",
    methods=["GET", "POST"]
)
@login_required
def add_availability():

    if request.method == "POST":

        faculty_id = request.form.get("faculty")
        timeslot_id = request.form.get("timeslot")
        available_value = request.form.get("available")

        # Basic validation
        if not faculty_id or not timeslot_id:
            flash(
                "Please select faculty and time slot.",
                "danger"
            )

            return redirect(
                url_for("availability.add_availability")
            )

        available = (
            available_value == "Yes"
        )

        # Prevent duplicate faculty + timeslot
        existing = FacultyAvailability.query.filter_by(
            faculty_id=faculty_id,
            timeslot_id=timeslot_id
        ).first()

        if existing:

            flash(
                "Availability for this faculty and time slot already exists.",
                "warning"
            )

            return redirect(
                url_for("availability.add_availability")
            )

        record = FacultyAvailability(

            faculty_id=faculty_id,

            timeslot_id=timeslot_id,

            available=available
        )

        db.session.add(record)

        db.session.commit()

        flash(
            "Faculty availability added successfully.",
            "success"
        )

        return redirect(
            url_for("availability.availability")
        )

    faculty = Faculty.query.order_by(
        Faculty.faculty_name
    ).all()

    timeslots = TimeSlot.query.order_by(
        TimeSlot.day,
        TimeSlot.period
    ).all()

    return render_template(
        "faculty_availability/add_availability.html",
        faculty=faculty,
        timeslots=timeslots
    )


# ---------------------------------------------------------
# DELETE AVAILABILITY
# ---------------------------------------------------------

@availability_bp.route(
    "/availability/delete/<int:id>"
)
@login_required
def delete_availability(id):

    record = FacultyAvailability.query.get_or_404(id)

    db.session.delete(record)

    db.session.commit()

    flash(
        "Faculty availability deleted successfully.",
        "success"
    )

    return redirect(
        url_for("availability.availability")
    )
