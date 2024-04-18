from flask import Blueprint, flash, g, render_template, request, redirect, url_for
from solar_offset.db import get_db
from solar_offset.utils.carbon_offset_util import SOLAR_PANEL_POWER_kW, calc_carbon_offset, calc_solar_panel_offset
from solar_offset.utils.misc import calculate_percentile, count_occurences, get_max_occurence, round_to_n_sig_figs
from solar_offset.utils.statistics_util import calculate_statistics

from math import floor, isclose

from solar_offset.views.auth import login_required

import hashlib





bp = Blueprint("householder", __name__)


@bp.route("/householder")
@login_required("h")
def dashboard():
    db = get_db()

    user_footprint = g.user['householder_carbon_footprint']
    carbon_offset_data = dict()
    if user_footprint:
        user_donations_countries = db.execute(
            "SELECT electricity_mix_percentage, solar_hours, electricty_consumption, \
                carbon_emissions, solar_panel_price_per_kw, donation.* \
                FROM country JOIN donation \
                ON (country.country_code == donation.country_code) \
                WHERE householder_id == ?;"
            , [g.user['id']]).fetchall()
        calc_offset = sum([ calc_carbon_offset(cd) * cd['donation_amount'] / 1000000 for cd in user_donations_countries ])
        carbon_offset_data = {
            'donation_offset': round(calc_offset * 1000, 2), # Convert from tons to kg
            'reduction_percent': round(calc_offset / user_footprint * 100, 2),
            'reduced_footprint': round(user_footprint - calc_offset, 2)
        }

    donations = db.execute(
        "SELECT donation.*, \
            country.name AS country_name, country.short_code AS country_short_code, \
            country.solar_panel_price_per_kw AS kw_panel_price, organization.name AS orga_name \
            FROM donation JOIN country JOIN organization \
            ON (country.country_code == donation.country_code AND organization.name_slug == donation.organization_slug) \
            WHERE donation.householder_id == ? \
            ORDER BY donation.created DESC", [g.user['id']]).fetchall()
    donations = [ dict(d) for d in donations ]
    for d in donations:
        d['created_date'] = d['created'].date()
        d['donation_panels'] = round(d['donation_amount'] / (SOLAR_PANEL_POWER_kW * d['kw_panel_price']))

    stats = calculate_statistics()

    stats_dict = dict()
    stats_dict['count_countries'] = len(set([ d['country_code'] for d in donations ]))
    if donations:
        stats_dict['dominant_country'] = get_max_occurence(count_occurences([d['country_name'] for d in donations]))
        stats_dict['donated_panels'] = sum([ d['donation_panels'] for d in donations ])
        stats_dict['donated_sum'] = sum([ d['donation_amount'] for d in donations ])

    return render_template(
        "/users/householder/householderdashboard.html",
        statistics=stats,
        stats = stats_dict,
        carbon_offset_data=carbon_offset_data,
        donations=donations
    )

@bp.route("/householder/update_footprint", methods=['POST'])
@login_required("h")
def update_carbon_footprint():
    user_id = g.user['id']
    updated_footprint = request.form.get('footprint')

    if not updated_footprint:
        flash("carbon footprint not updated - you did not enter a value", "warning")
        return redirect(url_for('householder.dashboard'))

    try:
        updated_footprint = float(updated_footprint)
    except (ValueError, OverflowError):
        flash("Could not update your carbon footprint - the value you gave was ill-formatted", "danger")
        return redirect(url_for('householder.dashboard'))
    
    if updated_footprint < 0:
        flash("Could not update your carbon footprint - you must give a positive value", "danger")
        return redirect(url_for('householder.dashboard'))
    elif isclose(updated_footprint, 0):
        flash("carbon footprint not updated - you entered a value of 0", "warning")
        return redirect(url_for('householder.dashboard'))

    db = get_db()
    db.execute("UPDATE user SET householder_carbon_footprint = ? WHERE id == ?", [updated_footprint, user_id])
    db.commit()

    flash("Your Carbon Footprint has been Updated!", "success")
    return redirect(url_for('householder.dashboard'))


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
        cd['solar_panel_price'] = round(cd['solar_panel_price_per_kw'] * SOLAR_PANEL_POWER_kW, 2)
        if isclose(cd['solar_panel_price'] % 1, 0):
            cd['solar_panel_price'] = int(cd['solar_panel_price'])
        cd['carbon_offset_per_pound'] = floor(calc_carbon_offset(c_row))
        cd['carbon_offset_per_panel_kg'] = round(calc_solar_panel_offset(c_row) / 1000.0, 1)
        cd['solar_panel_percent_footprint'] = None

        if cd['population_size'] >= 1000000000:
            cd['population_size'] = {'val': cd['population_size'], 'val_format': round(cd['population_size'] / 1000000000., 2), 'unit': "billion"}
        elif cd['population_size'] >= 1000000:
            cd['population_size'] = {'val': cd['population_size'], 'val_format': round(cd['population_size'] / 1000000., 2), 'unit': "million"}
        elif cd['population_size'] >= 10000:
            cd['population_size'] = {'val': cd['population_size'], 'val_format': round(cd['population_size'] / 1000., 2), 'unit': "thousand"}
        else:
            cd['population_size'] = {'val': cd['population_size'], 'val_format': cd['population_size'], 'unit': ""}

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

    if "raw" in request.args:
        for cd in country_dicts:
            cd.pop("description")
            cd.pop("electricty_consumption")
            cd.pop("short_code")
        return country_dicts
    else:
        return render_template(
            "./users/householder/country_list.html",
            countries=sorted(country_dicts, key=lambda c: c['carbon_offset_per_panel_kg'], reverse=True)
        )


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




@bp.route("/referal/<sender>/<recipient>")
def referal(sender, recipient):
    welcome_message = f"Hello, {recipient}! Welcome, sent by {sender}!"
    return render_template("referal.html", message=welcome_message)











