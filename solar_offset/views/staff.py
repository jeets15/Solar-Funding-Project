from flask import Blueprint, render_template, request
from solar_offset.db import get_db
from solar_offset.views.auth import login_required

bp = Blueprint("staff", __name__)


@bp.route("/staff", methods=["GET", "POST"])
@login_required("s")
def staff():
    db = get_db()
    user_types = ["admin", "householder", "staff"]
    countries = db.execute(
        "SELECT country.name as name, country.country_code as country_code, organization.name as org_name \
            FROM country JOIN organization \
            ON country.country_code = organization.country_code;"
    ).fetchall()
    return render_template("users/staff/staffdashboard.html", countries=countries)


@bp.route("/staff/report/", methods=["POST"])
@login_required("s")
def report():
    db = get_db()

    country = request.form['country']
    organization = request.form['organization']

    query = """
        SELECT u.email_username AS name, c.name AS country_name, o.name AS organization_name, SUM(d.donation_amount) AS total_donation_amount
        FROM user u
        JOIN donation d ON u.id = d.householder_id
        JOIN country c ON c.country_code = d.country_code
        JOIN organization o ON d.country_code = o.country_code AND d.organization_slug = o.name_slug
        WHERE c.name = ? AND o.name = ?
        GROUP BY u.id, c.name, o.name;
        """
    users = db.execute(query, (country, organization)).fetchall()

    return render_template("users/staff/report.html", users=users)
