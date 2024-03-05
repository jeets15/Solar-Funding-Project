from math import floor
from flask import Blueprint, render_template

from solar_offset.db import get_db
from solar_offset.util import calc_carbon_offset

bp = Blueprint("householder", __name__)

@bp.route("/")
def home():
    return render_template("householder/home.html")

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
            GROUP BY country.country_code;"
    ).fetchall()

    country_dicts = []
    for c_row in countries:
        cd = dict(c_row)
        cd["carbon_offset"] = floor(calc_carbon_offset(c_row))
        country_dicts.append(cd)

    return render_template("householder/country_list.html", countries=country_dicts)

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/register")
def register():
    return render_template("register.html")