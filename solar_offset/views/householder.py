from flask import Blueprint, render_template

from solar_offset.db import get_db

bp = Blueprint("householder", __name__)

@bp.route("/")
def home():
    return render_template("/home.html")

@bp.route("/about")
def about():
    return "Hello, About!"

@bp.route("/countries")
def country_list():
    # TODO Make sure that the countries coming back are sorted (in some way)
    # TODO Change SQL query to also include the number of donations and the total funds donated for each country
    db = get_db()
    countries = db.execute(
        "SELECT * FROM country;"
    ).fetchall()
    return render_template("householder/country_list.html", countries=countries)

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/register")
def register():
    return render_template("register.html")