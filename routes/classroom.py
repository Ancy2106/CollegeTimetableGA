from flask import Blueprint, render_template, request, redirect, url_for

from models import db
from models.classroom import Classroom
from utils.auth import login_required

classroom_bp = Blueprint(
    "classroom",
    __name__
)


@classroom_bp.route("/classrooms")
@login_required
def classrooms():

    rooms = Classroom.query.order_by(
        Classroom.room_number
    ).all()

    return render_template(
        "classroom/classrooms.html",
        classrooms=rooms
    )


@classroom_bp.route(
    "/classrooms/add",
    methods=["GET", "POST"]
)
@login_required
def add_classroom():

    if request.method == "POST":

        room = Classroom(

            room_number=request.form["room_number"],
            room_name=request.form["room_name"],
            room_type=request.form["room_type"],
            capacity=request.form["capacity"],
            building=request.form["building"],
            floor=request.form["floor"],
            availability=request.form["availability"]

        )

        db.session.add(room)
        db.session.commit()

        return redirect(
            url_for("classroom.classrooms")
        )

    return render_template(
        "classroom/add_classroom.html"
    )


@classroom_bp.route("/classrooms/delete/<int:id>")
@login_required
def delete_classroom(id):

    room = Classroom.query.get_or_404(id)

    db.session.delete(room)

    db.session.commit()

    return redirect(
        url_for("classroom.classrooms")
    )
