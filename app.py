from models.semester import Semester
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from config import Config
from models import db

# Models
from models.faculty import Faculty
from models.subject import Subject
from models.classroom import Classroom
from models.department import Department
from models.timeslot import TimeSlot
from models.timetable import Timetable
from models.admin import Admin
from models.semester import Semester
from models.section import Section
from models.subject_allocation import SubjectAllocation
from models.faculty_availability import FacultyAvailability

# Blueprints
from routes.faculty import faculty_bp
from routes.subject import subject_bp
from routes.department import department_bp
from routes.classroom import classroom_bp
from routes.timeslot import timeslot_bp
from routes.semester import semester_bp
from routes.section import section_bp
from routes.subject_allocation import allocation_bp
from routes.faculty_availability import availability_bp
from routes.timetable import timetable_bp

from utils.auth import login_required

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

# Register Blueprints
app.register_blueprint(faculty_bp)
app.register_blueprint(subject_bp)
app.register_blueprint(department_bp)
app.register_blueprint(classroom_bp)
app.register_blueprint(timeslot_bp)
app.register_blueprint(semester_bp)
app.register_blueprint(section_bp)
app.register_blueprint(allocation_bp)
app.register_blueprint(availability_bp)
app.register_blueprint(timetable_bp)

with app.app_context():
    db.create_all()


# -------------------------------
# Login Page
# -------------------------------
@app.route("/")
def home():

    # Already logged in
    if session.get("logged_in"):
        return redirect(url_for("dashboard"))

    return render_template("auth/login.html")


# -------------------------------
# Login
# -------------------------------
@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    admin = Admin.query.filter_by(
        username=username,
        password=password
    ).first()

    if admin:

        session["logged_in"] = True
        session["admin_name"] = admin.full_name
        session["admin_role"] = admin.role

        return redirect(url_for("dashboard"))

    return render_template(
        "auth/login.html",
        error="Invalid Username or Password"
    )


# -------------------------------
# Dashboard
# -------------------------------
@app.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard/dashboard.html",

        faculty_count=Faculty.query.count(),

        subject_count=Subject.query.count(),

        classroom_count=Classroom.query.count(),

        department_count=Department.query.count(),

        semester_count=Semester.query.count(),

        section_count=Section.query.count(),

        timeslot_count=TimeSlot.query.count(),

        timetable_count=Timetable.query.count(),

        allocation_count=SubjectAllocation.query.count(),

        availability_count=FacultyAvailability.query.count()
    )

# -------------------------------
# Logout
# -------------------------------


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
