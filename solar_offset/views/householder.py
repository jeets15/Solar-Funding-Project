from flask import Blueprint, render_template

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

@bp.route("/register")
def register():
    return render_template("register.html")



@bp.route("/countries/projects")
def projects():
    # Assuming you want to render projects.html without specific country data
    return render_template("householder/projects.html")

@bp.route('/countries/projects/<country_code>')
def projects_by_country(country_code):
    # Connect to the database
    db = get_db()
    cursor = db.cursor()

    # Fetch country description from the database
    cursor.execute("SELECT description FROM countryinfo WHERE country_code = ?", (country_code,))
    country_description = cursor.fetchone()

    # Fetch projects for the selected country from the database
    cursor.execute("SELECT name, description, sites, status "
                   "FROM projects "
                   "WHERE country_code = ?", (country_code,))
    projects = cursor.fetchall()

    # Close the database cursor
    cursor.close()

    return render_template("householder/projects.html", country_code=country_code, projects=projects, country_description=country_description)

