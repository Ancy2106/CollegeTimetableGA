from flask import Blueprint, render_template, request, redirect, url_for

from models import db
from models.timeslot import TimeSlot
from utils.auth import login_required

timeslot_bp = Blueprint(
    "timeslot",
    __name__
)


@timeslot_bp.route("/timeslots")
@login_required
def timeslots():

    slots = TimeSlot.query.order_by(
        TimeSlot.day,
        TimeSlot.period
    ).all()

    return render_template(
        "timeslot/timeslots.html",
        timeslots=slots
    )


@timeslot_bp.route(
    "/timeslots/add",
    methods=["GET", "POST"]
)
@login_required
def add_timeslot():

    if request.method == "POST":

        slot = TimeSlot(

            day=request.form["day"],

            period=request.form["period"],

            start_time=request.form["start_time"],

            end_time=request.form["end_time"],

            session=request.form["session"]

        )

        db.session.add(slot)

        db.session.commit()

        return redirect(
            url_for("timeslot.timeslots")
        )

    return render_template(
        "timeslot/add_timeslot.html"
    )


@timeslot_bp.route("/timeslots/delete/<int:id>")
@login_required
def delete_timeslot(id):

    slot = TimeSlot.query.get_or_404(id)

    db.session.delete(slot)

    db.session.commit()

    return redirect(
        url_for("timeslot.timeslots")
    )


@timeslot_bp.route("/timeslots/generate")
@login_required
def generate_default_timeslots():

    TimeSlot.query.delete()

    db.session.commit()

    schedule = [

        ("1", "09:00", "10:00", "Morning"),

        ("2", "10:00", "11:00", "Morning"),

        ("3", "11:00", "12:00", "Morning"),

        ("4", "12:00", "01:00", "Afternoon"),

        ("5", "01:00", "02:00", "Afternoon"),

        ("6", "02:00", "03:00", "Afternoon"),

        ("7", "03:00", "04:00", "Afternoon")

    ]

    days = [

        "Monday",

        "Tuesday",

        "Wednesday",

        "Thursday",

        "Friday"

    ]

    for day in days:

        for period, start, end, session in schedule:

            slot = TimeSlot(

                day=day,

                period=int(period),

                start_time=start,

                end_time=end,

                session=session

            )

            db.session.add(slot)

    db.session.commit()

    return redirect(url_for("timeslot.timeslots"))
