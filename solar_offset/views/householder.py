from flask import Blueprint, render_template,flash
from solar_offset import get_db
from werkzeug.security import check_password_hash, generate_password_hash

from solar_offset.db import get_db

bp = Blueprint("householder", __name__)

@bp.route("/")
def home():
    return render_template("householder/home.html")

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

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/register",methods=["GET","POST"])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        email = request.form['emailaddress']
        password = request.form['password']
        db = get_db()
        error = None

        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (userid, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {userid} is already registered."
        else:
            return redirect(url_for("login"))

        flash(error)

    return render_template('register.html')

