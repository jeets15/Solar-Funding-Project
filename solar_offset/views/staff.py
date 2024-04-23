# from flask import Blueprint, render_template, request
# from solar_offset.db import get_db
# from solar_offset.views.auth import login_required

# bp = Blueprint("staff", __name__)


# @bp.route("/staff", methods=["GET", "POST"])
# @login_required("s")
# def staff():
#     db = get_db()
#     user_types = ["admin", "householder", "staff"]
#     countries = db.execute(
#         "SELECT country.name as name, country.country_code as country_code, organization.name as org_name \
#             FROM country JOIN organization \
#             ON country.country_code = organization.country_code;"
#     ).fetchall()
#     return render_template("users/staff/staffdashboard.html", countries=countries)


# @bp.route("/staff/report/", methods=["POST"])
# @login_required("s")
# def report():
#     db = get_db()

#     country = request.form['country']
#     organization = request.form['organization']

#     query = """
#         SELECT u.email_username AS name, c.name AS country_name, o.name AS organization_name, SUM(d.donation_amount) AS total_donation_amount
#         FROM user u
#         JOIN donation d ON u.id = d.householder_id
#         JOIN country c ON c.country_code = d.country_code
#         JOIN organization o ON d.country_code = o.country_code AND d.organization_slug = o.name_slug
#         WHERE c.name = ? AND o.name = ?
#         GROUP BY u.id, c.name, o.name;
#         """
#     users = db.execute(query, (country, organization)).fetchall()

#     return render_template("users/staff/report.html", users=users)


from flask import Blueprint, render_template, request, jsonify, make_response
from solar_offset.db import get_db
from solar_offset.views.auth import login_required
import pdfkit

bp = Blueprint("staff", __name__)

@bp.route("/staff", methods=["GET"])
@login_required("s")
def staff():
    db = get_db()
    countries = db.execute(
        "SELECT country.name AS name, country.country_code AS country_code FROM country;"
    ).fetchall()
    return render_template("./users/staff/staffdashboard.html", countries=countries)


@bp.route("/staff/organizations/<value>", methods=["GET", "POST"])
@login_required("s")
def get_organizations(value):
    db = get_db()
    organizations = db.execute(
        "SELECT organization.name AS name FROM organization \
        JOIN country ON organization.country_code = country.country_code \
        WHERE country.country_code = ?;",
        (value,)
    ).fetchall()

    # Convert Row objects to dictionaries
    organizations_data = [dict(org) for org in organizations]

    return jsonify(organizations_data) # Return JSON response

@bp.route("/staff/report", methods=["POST"])
@login_required("s")
def generate_report():
    db = get_db()
    country_code = request.form["country"]
    organization_name = request.form["organization"]
    users = db.execute(
        "SELECT u.email_username AS name, c.name AS country_name, o.name AS organization_name, SUM(d.donation_amount) AS total_donation_amount \
        FROM user u \
        JOIN donation d ON u.id = d.householder_id \
        JOIN country c ON c.country_code = d.country_code \
        JOIN organization o ON d.organization_slug = o.name_slug AND c.country_code = o.country_code \
        WHERE c.country_code = ? AND o.name = ? \
        GROUP BY u.id, c.name, o.name;",
        (country_code, organization_name),
    ).fetchall()
    return render_template("./users/staff/report.html", users=users)

# @bp.route("/staff/report", methods=["POST"])
# @login_required("s")
# def generate_report():
#     db = get_db()
#     country_code = request.form["country"]
#     organization_name = request.form["organization"]
#     users = db.execute(
#         "SELECT u.email_username AS name, c.name AS country_name, o.name AS organization_name, SUM(d.donation_amount) AS total_donation_amount \
#          FROM user u \
#          JOIN donation d ON u.id = d.householder_id \
#          JOIN country c ON c.country_code = d.country_code \
#          JOIN organization o ON d.organization_slug = o.name_slug AND c.country_code = o.country_code \
#          WHERE c.country_code = ? AND o.name = ? \
#          GROUP BY u.id, c.name, o.name;",
#         (country_code, organization_name),
#     ).fetchall()

#     # Render only the report table body with data
#     report_data = render_template("./users/staff/report_table_body.html", users=users)
#     return report_data  # Return the rendered table body HTML

@bp.route("/staff/export", methods=["POST"])
@login_required("s")
def export_report():
    db = get_db()
    country_code = request.form["country"]
    organization_name = request.form["organization"]
    users = db.execute(
        "SELECT u.email_username AS name, c.name AS country_name, o.name AS organization_name, SUM(d.donation_amount) AS total_donation_amount \
        FROM user u \
        JOIN donation d ON u.id = d.householder_id \
        JOIN country c ON c.country_code = d.country_code \
        JOIN organization o ON d.organization_slug = o.name_slug AND c.country_code = o.country_code \
        WHERE c.country_code = ? AND o.name = ? \
        GROUP BY u.id, c.name, o.name;",
        (country_code, organization_name),
    ).fetchall()

    # Render HTML template with report data
    html = render_template("./users/staff/export_report.html", users=users)

    # Convert HTML to PDF
    pdf = pdfkit.from_string(html, False)

    # Create response with PDF content
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=report.pdf"

    return response

