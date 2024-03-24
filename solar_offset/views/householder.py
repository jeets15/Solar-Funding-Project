from flask import Blueprint, g, render_template, request, redirect, url_for
from solar_offset.db import get_db
from solar_offset.utils.carbon_offset_util import SOLAR_PANEL_POWER_kW, calc_carbon_offset, calc_solar_panel_offset
from solar_offset.utils.misc import calculate_percentile, round_to_n_sig_figs
from solar_offset.utils.statistics_util import calculate_statistics

from math import floor

from solar_offset.views.auth import login_required

bp = Blueprint("householder", __name__)


@bp.route("/householder")
@login_required("h")
def dashboard():
    stats = calculate_statistics()
    return render_template(
        "/users/householder/householderdashboard.html",
        statistics=stats
    )


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
        cd['avg_solar_hours'] = round(cd['solar_hours'] / 365, 1)
        cd['solar_panel_price'] = round(cd['solar_power_price'] * SOLAR_PANEL_POWER_kW, 2)
        cd['carbon_offset_per_pound'] = floor(calc_carbon_offset(c_row))
        cd['carbon_offset_per_panel_kg'] = round(calc_solar_panel_offset(c_row) / 1000.0, 1)
        cd['solar_panel_percent_footprint'] = None
        if g.get("user", None):
            if g.user.get('householder_carbon_footprint', None):
                # Calculate Percentage of how much carbon footprint is reduced by donating one solar panel
                fraction_footprint_reduction = cd['carbon_offset_per_panel_kg'] / (g.user['householder_carbon_footprint'] * 1000)
                # round to 3 significant figures, convert to percent, then ensure that percentage only has 2 decimal places
                cd['solar_panel_percent_footprint'] = round(round_to_n_sig_figs(fraction_footprint_reduction, 3) * 100, 2)
        country_dicts.append(cd)

    # Give traffic light indicator according to carbon_offset
    # Green ~ upper 30%, Red ~ lower 30%, Amber ~ Midfield
    lst_offset_vals = [ c['carbon_offset_per_pound'] for c in country_dicts ]
    upper_bound = calculate_percentile(lst_offset_vals, 0.7)
    lower_bound = calculate_percentile(lst_offset_vals, 0.3)
    for country in country_dicts:
        if country['carbon_offset_per_pound'] >= upper_bound:
            country['signal_color'] = "green"
        elif country['carbon_offset_per_pound'] <= lower_bound:
            country['signal_color'] = "red"
        else:
            country['signal_color'] = "amber"

    # TODO sorting functionality

    if "raw" in request.args:
        for cd in country_dicts:
            cd.pop("description")
            cd.pop("electricty_consumption")
            cd.pop("short_code")
        return country_dicts
    else:
        return render_template("./users/householder/country_list.html", countries=country_dicts)


@bp.route("/countries/<country_code>")
def country(country_code):
    country_code = str(country_code).upper()

    db = get_db()
    country = db.execute("SELECT * FROM country WHERE country_code == ?", [country_code]).fetchone()
    country = dict(country)
    country["descriptions"] = [d.strip() for d in country["description"].split(r"\n")]

    # If country doesn't exist in database, redirect to countries view
    if country is None:
        return redirect(url_for('householder.country_list'))

    lst_orga = db.execute("SELECT * FROM organization WHERE country_code == ?", [country_code]).fetchall()
    lst_orga = [dict(orga) for orga in lst_orga]
    for orga in lst_orga:
        orga["descriptions"] = [d.strip() for d in orga["description"].split(r"\n")]

    return render_template(
        "./users/householder/projects.html",
        country=country,
        organizations=lst_orga)
