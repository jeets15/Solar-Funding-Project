from datetime import datetime
from flask import Blueprint, render_template, flash, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from solar_offset.db import get_db
from solar_offset.util import calc_carbon_offset

from math import floor
from uuid import uuid4

bp = Blueprint("householder", __name__)


@bp.route("/")
def home():
    return render_template("householder/home.html")


@bp.route("/householder")
def dashboard():
    username = session.get('username')
    return render_template("householder/householderdashboard.html", username=username)


@bp.route("/about")
def about():
    return "Hello, About!"


@bp.route("/countries")
def country_list():
    db = get_db()
    countries = db.execute(
        "SELECT country.*, COUNT(donation_amount) AS donation_count, SUM(donation_amount) AS donation_sum \
            FROM country LEFT JOIN donation \
            ON (country.country_code == donation.country_code) \
            GROUP BY country.country_code \
            ORDER BY country.name ASC;"
    ).fetchall()

    country_dicts = []
    for c_row in countries:
        cd = dict(c_row)
        if not cd["donation_sum"]:
            cd["donation_sum"] = 0
        cd["carbon_offset"] = floor(calc_carbon_offset(c_row))
        country_dicts.append(cd)

    if "raw" in request.args:
        for cd in country_dicts:
            cd.pop("description")
            cd.pop("electricty_consumption")
            cd.pop("short_code")
        return country_dicts
    else:
        return render_template("householder/country_list.html", countries=country_dicts)
    
@bp.route("/countries/<country_code>")
def country(country_code):
    return country_code


@bp.route("/api/donate", methods=["GET", "POST"])
def donate():
    if request.method == 'POST':
        # Ensure that user is logged into a session
        sess_user_id = session.get("user_id", None)
        if sess_user_id is None:
            return "You must be logged in to donate", 401
        
        # Fetch user record from database
        db = get_db()
        print(sess_user_id)
        user_entry = db.execute("SELECT * FROM user WHERE user.id == ?", [sess_user_id]).fetchone()

        # Check that the user id exists in the database (could be forged)
        if user_entry is None:
            return "Invalid User Credentials", 400
        
        # Ensure that the only user role that this user has is 'h' (householder)
        if len(user_entry["user_type"].replace("h", "").replace("_", "")) > 0:
            return "Only Householder accounts are allowed to donate", 403
        
        # Validate the Form Entries
        country_code = request.form["country_code"]
        if db.execute(
            "SELECT country_code FROM country WHERE country.country_code == ?", [country_code]
            ).fetchone() is None:
            return "Specified Country does not Exist", 400
        organization_slug = request.form["organization_slug"]
        if db.execute(
            "SELECT name_slug, country_code FROM organization WHERE name_slug == ? AND country_code == ?", [organization_slug, country_code]
            ).fetchone() is None:
            return "Specified Organization does not Exist", 400
        donation_amount = request.form["donation_amount"]
        if not donation_amount.isdigit():
            return "Donation Amount must be a positive integer", 400
        else:
            donation_amount = int(donation_amount)
        if donation_amount < 1 \
            or donation_amount != int(donation_amount):
            return "Donation Amount must be a positive integer", 400

        # Insert new Donation into the Database
        timestamp_now = datetime.now()
        db.execute(
            "INSERT INTO donation (created, householder_id, country_code, organization_slug, donation_amount) \
            VALUES (?, ?, ?, ?, ?);",
            [timestamp_now, sess_user_id, country_code, organization_slug, donation_amount]
        )
        db.commit()
        return {"success": True}, 200
    
    else:
        organization_slug = request.args.get('orga', None)
        country_code = request.args.get('country', None)
        if organization_slug is None:
            return "No Organization given", 400
        elif country_code is None:
            return "No Country code given", 400
        
        organization_slug = organization_slug.lower()
        country_code = country_code.upper()
        
        db = get_db()
        country = db.execute("SELECT * FROM country WHERE country_code == ?", [country_code]).fetchone()
        organization = db.execute(
            "SELECT * FROM organization WHERE name_slug == ? AND country_code == ?", [organization_slug, country_code]
            ).fetchone()
        if country is None:
            return "Country Code does not exist", 400
        elif organization is None:
            return "Organization does not exist", 400
        else:
            return render_template(
                "householder/donate.html",
                country=country,
                organization=organization)


@bp.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form["emailusrname"]
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM user WHERE email_username = ?', (username,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username!!'
        elif check_password_hash(user['password_hash'], password) == False:
            error = 'Incorrect password!!'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            if (user['display_name'] is not None):
                session['username'] = user['display_name']
            else:
                session['username'] = user['email_username']

            usertype = user["user_type"]

            if (usertype == "householder"):
                flash("User login succesfull!", "success")
                return redirect(url_for("householder.dashboard"))
            elif (usertype == "staff"):
                flash("Staff login succesfull!", "success")
                return redirect(url_for("staff.staff"))
            else:
                flash("Admin login succesfull!", "success")
                return redirect(url_for("admin.admin"))

        flash(error, "danger")
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        if (request.form['username'] != ""):
            username = request.form['username']
        email = request.form['emailaddress']
        password = request.form['password']
        db = get_db()
        error = None
        userid = str(uuid4())
        try:
            if (username != ""):
                db.execute(
                    "INSERT INTO user (id, email_username, password_hash, user_type,display_name) VALUES (?,?,?,?,?)",
                    (userid, email, generate_password_hash(password), "householder", username),
                )
            else:

                db.execute(
                    "INSERT INTO user (id, email_username, password_hash, user_type) VALUES (?,?,?,?)",
                    (userid, email, generate_password_hash(password), "householder"),
                )
            db.commit()
        except db.IntegrityError:
            error = f"Email ID: {email} is already registered."
        else:
            session.clear()
            session["user_id"] = userid
            if (username != ""):
                session["username"] = username
            else:
                session["username"] = email
            flash("User registered succesfully!", "success")
            return redirect(url_for("householder.dashboard"))

        print("Error", error)

    return render_template('./register.html')
