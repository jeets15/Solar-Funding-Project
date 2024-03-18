from flask import Blueprint, render_template, request, session
from solar_offset.db import get_db
from solar_offset.util import calc_carbon_offset

from math import floor

bp = Blueprint("staff", __name__)


# @bp.route("/staff", methods=["GET", "POST"])
# def staff():
#     staffname = session.get('username')
#     is_logged_in = True if staffname else False
#     return render_template("./staff/staffdashboard.html", staffname=staffname, is_logged_in=is_logged_in)
# "SELECT country.*, COUNT(donation_amount) AS donation_count, SUM(donation_amount) AS donation_sum \
#             FROM country LEFT JOIN donation \
#             ON (country.country_code == donation.country_code) \
#             GROUP BY country.country_code \
#             ORDER BY country.name ASC;"



@bp.route("/staff/report")
def report():
    staffname = session.get('username')
    db = get_db()
    is_logged_in = True if staffname else False
    user_types = ["admin", "householder", "staff"]
    print(is_logged_in)
    # users = db.execute(
    #     'SELECT * FROM user WHERE user_type NOT LIKE ? ', ('%a%',)
    # ).fetchall()
    users = db.execute(
        "SELECT u.email_username, c.name AS country_name, o.name AS organization_name, SUM(d.donation_amount) AS total_donation_amount \
            FROM user u \
            JOIN donation d ON u.id = d.householder_id \
            JOIN organization o ON d.country_code = o.country_code AND d.organization_slug = o.name_slug \
            JOIN country c ON d.country_code = c.country_code \
            GROUP BY u.email_username, c.name, o.name;"
    ).fetchall()
    # user_dicts = []
    # for user_row in users:
    #     userdict = dict(user_row)
    #     if ("h__" in userdict["user_type"]):
    #         userdict["user_type"] = "householder"
    #     else:
    #         userdict["user_type"] = "staff"
    #     user_dicts.append(userdict)
    return render_template("./staff/report.html", users=users, staffname=staffname, is_logged_in=is_logged_in)



@bp.route("/staff")
def staff():
    staffname = session.get('username')
    db = get_db()
    is_logged_in = True if staffname else False
    user_types = ["admin", "householder", "staff"]
    print(is_logged_in)

    # Fetch all countries and associated organizations from the database
    countries = db.execute(
        "SELECT country.*, COUNT(donation_amount) AS donation_count, SUM(donation_amount) AS donation_sum \
            FROM country LEFT JOIN donation \
            ON (country.country_code == donation.country_code) \
            GROUP BY country.country_code \
            ORDER BY country.name ASC;"
    ).fetchall()

    # Fetch all users from the database and prepare the data
    users = db.execute(
        'SELECT * FROM user WHERE user_type NOT LIKE ? ', ('%a%',)
    ).fetchall()
    user_dicts = []
    for user_row in users:
        userdict = dict(user_row)
        if "h__" in userdict["user_type"]:
            userdict["user_type"] = "householder"
        else:
            userdict["user_type"] = "staff"
        user_dicts.append(userdict)

    return render_template("./staff/staffdashboard.html", countries=countries, staffname=staffname, users=user_dicts, is_logged_in=is_logged_in)



