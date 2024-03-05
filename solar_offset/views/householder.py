from flask import Flask, Blueprint, render_template, flash, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from solar_offset.db import get_db

app = Flask(__name__)
app.secret_key = 'hkekekkwlbmvjtj'
bp = Blueprint("householder", __name__)
from uuid import uuid4


@bp.route("/")
def home():
    return render_template("householder/home.html")


@bp.route("/householder")
def dashboard():
    username = session.get('user_id')
    return render_template("householder/householderdashboard.html", username=username)


@bp.route("/about")
def about():
    return "Hello, About!"


@bp.route("/countries")
def country_list():
    # TODO Add calculated Potential Carbon Offset for each country
    db = get_db()
    countries = db.execute(
        "SELECT country.*, COUNT(donation_amount) AS donation_count, SUM(donation_amount) AS donation_sum \
            FROM country LEFT JOIN donation \
            ON (country.country_code == donation.country_code) \
            GROUP BY country.country_code;"
    ).fetchall()
    country_dicts = [dict(c) for c in countries]
    return render_template("householder/country_list.html", countries=country_dicts)


@bp.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        db = get_db()
        error = None

        # If the user is admin, we dont query the db and just check the username
        user = db.execute(
            'SELECT * FROM householder WHERE display_name = ?', (userid,)
        ).fetchone()
        admin = db.execute(
            'SELECT * FROM administrator WHERE username = ?', (userid,)
        ).fetchone()
        staff = db.execute(
            'SELECT * FROM staff WHERE username = ?', (userid,)
        ).fetchone()
        if user is None and admin is None and staff is None:
            error = 'Incorrect username.'
        elif user is not None and not check_password_hash(user['password_hash'], password):
            error = 'Incorrect password.'
        elif staff is not None and not check_password_hash(staff['password_hash'], password):
            error = 'Incorrect password.'
        elif admin is not None and not check_password_hash(admin['password_hash'], password):
            error = 'Incorrect password.'
        if error is None and user is not None:
            session.clear()
            session['user_id'] = user['display_name']
            flash("User login succesfull!", "success")
            return redirect(url_for("householder.dashboard"))
        elif error is None and staff is not None:
            session.clear()
            session['staff_id'] = staff['username']
            flash("Staff login succesfull!", "success")
            return redirect(url_for("staff.staff"))
        elif error is None and admin is not None:
            session.clear()
            session['admin_id'] = admin['username']
            flash("Admin login succesfull!", "success")
            return redirect(url_for("admin.admin"))
        flash(error, "danger")
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        email = request.form['emailaddress']
        password = request.form['password']
        db = get_db()
        error = None

        try:
            db.execute(
                "INSERT INTO householder (id,email,display_name,password_hash) VALUES (?,?,?,?)",
                (str(uuid4()), email, userid, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {userid} is already registered."
        else:
            session.clear()
            session['user_id'] = userid
            flash("User registered succesfully!", "success")
            return redirect(url_for("householder.dashboard"))

        print("Error", error)

    return render_template('./register.html')
