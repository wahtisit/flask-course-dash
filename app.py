from flask import Flask, render_template, jsonify, request, redirect, url_for
from models import *

app = Flask(__name__)
server = app.server

db_path = os.path.join(os.path.dirname(__file__), 'database.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def create_app():
    return app

@app.route("/")
def index():
    return redirect((url_for('courses')))

@app.route("/courses", methods=["GET"])
def courses():
    courses = Course.query.all()
    return render_template("courses.html", courses=courses)

@app.route("/courses", methods=["POST"])
def add_course():
    """Add a course to a schedule."""

    # Get form information.
    course_id = request.form.get("course_id")
    name = request.form.get("name")
    semester = request.form.get("semester")
    category = request.form.get("category")
    credits = request.form.get("credits")

    course = Course()
    course.add_course(course_id,name,semester,category,credits)

    courses = Course.query.all()
    return render_template("courses.html",courses=courses)

@app.route("/courses/<string:course_id>", methods=["GET"])
def course_info(course_id):
    """ get info about a single course """
    course = db.session.query(Course).get(course_id)
    course_json = jsonify(course.as_dict())
    print(course_json)
    return course_json

@app.route("/remove_course", methods=["POST", "GET"])
def remove_course():
    if request.method == 'GET':
        return redirect(url_for('courses'))
    
    course_id = request.form.get("course_id")
    
    Course.query.filter_by(course_id=course_id).delete()
    db.session.commit()

    print(f"Removing {course_id} from table courses")

    courses = Course.query.all()
    return render_template("courses.html", courses=courses)

@app.route("/schedules", methods=["GET"])
def schedules():
    schedules = db.session.query(Schedule).all()
    #courses = Course.query.all()
    courses = db.session.query(Course).filter(~Course.booked_in.any())
    
    return render_template("schedules.html", schedules=schedules, courses=courses)

@app.route("/schedules", methods=["POST"])
def add_schedule():
    course_id = request.form.get("course_id")
    year = request.form.get("year")
    realm = request.form.get("realm")
    minorMajor = request.form.get("minorMajor")

    semester = db.session.query(Course).get(course_id).semester

    schedule = Schedule(course_id=course_id, year=year, realm=realm, minorMajor=minorMajor, semester=semester)
    db.session.add(schedule)
    db.session.commit()

    return redirect(url_for('schedules'))

@app.route("/remove_schedule", methods=["GET", "POST"])
def remove_schedule():
    if request.method == 'GET':
        return redirect(url_for('courses'))

    schedule_id = request.form.get("schedule_id")
    
    Schedule.query.filter_by(id=schedule_id).delete()
    db.session.commit()

    print(f"Removing {schedule_id} from table schedules")
    return redirect(url_for('schedules'))

@app.route("/flights")
def flights():
    """List all flights."""
    flights = Flight.query.all()
    return render_template("flights.html", flights=flights)


@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """List details about a single flight."""

    # Make sure flight exists.
    flight = Flight.query.get(flight_id)
    if flight is None:
        return render_template("error.html", message="No such flight.")

    # Get all passengers.
    passengers = flight.passengers
    return render_template("flight.html", flight=flight, passengers=passengers)


@app.route("/api/flights/<int:flight_id>")
def flight_api(flight_id):
    """Return details about a single flight."""

    # Make sure flight exists.
    flight = Flight.query.get(flight_id)
    if flight is None:
        return jsonify({"error": "Invalid flight_id"}), 422

    # Get all passengers.
    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
            "origin": flight.origin,
            "destination": flight.destination,
            "duration": flight.duration,
            "passengers": names
        })
