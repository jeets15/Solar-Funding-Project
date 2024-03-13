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



@bp.route("/projects")
def projects():
    # Assuming you want to render projects.html without specific country data
    return render_template("householder/projects.html")

# Sample data for projects
project_data = {
    'ESP': [
        {
            'project_name': 'Solar Power Plant Installation',
            'description': 'A project to install a solar power plant in California.',
            'budget': '$1,000,000',
            'status': 'Ongoing'
        },
        {
            'project_name': 'Renewable Energy Research Center',
            'description': 'Establishment of a research center for renewable energy technologies.',
            'budget': '$500,000',
            'status': 'Planned'
        }
    ],
    'India': [
        {
            'project_name': 'Rural Electrification Initiative',
            'description': 'Electrification of remote villages using solar energy.',
            'budget': '₹50,00,000',
            'status': 'Completed'
        },
        {
            'project_name': 'Smart Cities Project',
            'description': 'Development of smart cities with renewable energy infrastructure.',
            'budget': '₹1,000,000,000',
            'status': 'In Progress'
        }
    ]
}

@bp.route('/projects/<country_code>')
def projects_by_country(country_code):
    country_projects = project_data.get(country_code)
    return render_template('householder/projects.html', country_code=country_code, projects=country_projects)


