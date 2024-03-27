from flask import Blueprint, g, render_template, request, redirect, url_for
from solar_offset.db import get_db
from solar_offset.utils.carbon_offset_util import SOLAR_PANEL_POWER_kW, calc_carbon_offset, calc_solar_panel_offset
from solar_offset.utils.misc import calculate_percentile, round_to_n_sig_figs
from solar_offset.utils.statistics_util import calculate_statistics

from math import floor, isclose

from solar_offset.views.auth import login_required

import hashlib





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














# Dummy database to simulate referral codes
referral_codes = {
    'REFCODE_47fa9dc4': 'jeetsinghvi@hotmail.com',
    'REFCODE_1234567890': 'jane.doe@example.com'
}


@bp.route('/generate_referral_code', methods=['GET'])
def generate_referral_code():
    email = ('jeetsinghvi@hotmail.com')      # Replace with email from database
    if email:
        email = email.strip()
        referral_code = generate_code_from_email(email)
        return f"Referral code for {email}: {referral_code}"
    else:
        return "Email parameter is missing"


def generate_code_from_email(email):
    # Add a unique identifier (e.g., user ID) to the email before hashing
    unique_identifier = '8b1a1136-0024-477f-9e29-cb7266cb46d6'
    email_with_id = email + unique_identifier

    # Use SHA-256 hashing to generate a unique hash for the email with ID
    hashed_email = hashlib.sha256(email_with_id.encode()).hexdigest()
    # Take the first 12 characters of the hashed email as the referral code
    referral_code = hashed_email[:12]
    return referral_code


@bp.route('/verify_referral_code', methods=['POST'])
def verify_referral_code():
    user_referral_code = request.form.get('referral_code')
    user_email = request.form.get('user_email')

    if user_referral_code:
        # Here, you would typically check the user's input against a database of valid referral codes
        if user_referral_code in referral_codes:
            referred_email = referral_codes[user_referral_code]
            # Apply discount to both users
            apply_discount_to_user(user_email, 0.1)  # 10% discount
            apply_discount_to_user(referred_email, 0.1)  # 10% discount
            return f"Discount applied for {user_email} and {referred_email}"
        else:
            return "Invalid referral code"
    else:
        return "Referral code not provided"

def apply_discount_to_user(email, discount):
    # Code to apply discount to the user with the given email
    pass  # Placeholder for actual implementation

