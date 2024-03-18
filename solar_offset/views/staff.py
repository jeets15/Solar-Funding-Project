from flask import Blueprint, render_template, request, session
from solar_offset.db import get_db

from math import floor

bp = Blueprint("staff", __name__)


@bp.route("/staff", methods=["GET", "POST"])
def staff():
    staffname = session.get('username')
    db = get_db()
    is_logged_in = True if staffname else False
    user_types = ["admin", "householder", "staff"]
    print(is_logged_in)
    countries = db.execute(
        "SELECT country.name as name, country.country_code as country_code, organization.name as org_name \
            FROM country JOIN organization \
            ON country.country_code = organization.country_code;"
    ).fetchall()
    return render_template("./staff/staffdashboard.html", countries=countries, staffname=staffname,
                           is_logged_in=is_logged_in)


@bp.route("/staff/report")
def report():
    staffname = session.get('username')
    db = get_db()
    is_logged_in = True if staffname else False
    users = db.execute(
        "SELECT u.email_username AS name, c.name AS country_name, o.name AS organization_name, SUM(d.donation_amount) AS total_donation_amount \
            FROM user u \
            JOIN donation d ON u.id = d.householder_id \
            JOIN organization o ON d.country_code = o.country_code AND d.organization_slug = o.name_slug \
            JOIN country c ON d.country_code = c.country_code \
            GROUP BY c.name, o.name;"
    ).fetchall()

    return render_template("./staff/report.html", users=users, is_logged_in=is_logged_in)
    if is_logged_in == False:
        return redirect("/login")
    return render_template("./users/staff/staffdashboard.html", staffname=staffname, is_logged_in=is_logged_in)
