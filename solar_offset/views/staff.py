from flask import Blueprint, render_template
from solar_offset.db import get_db
from solar_offset.utils.carbon_offset_util import SOLAR_PANEL_POWER_kW
from solar_offset.views.auth import login_required
bp = Blueprint("staff", __name__)

@bp.route("/staff", methods=["GET"])
@login_required("s")
def staff():
    db = get_db()
    donations_rows = db.execute(
        "SELECT donation.*, country.name AS country_name, country.solar_panel_price_per_kw, \
                organization.name AS organization_name, user.email_username AS householder \
            FROM donation JOIN country JOIN organization JOIN user \
            ON (donation.country_code == country.country_code) \
                AND (donation.organization_slug == organization.name_slug) \
                AND (donation.householder_id == user.id) \
            ORDER BY donation.created DESC;"
    ).fetchall()

    donations = []
    for d in donations_rows:
        donations.append(
            {
                'created': d['created'].strftime('%Y-%m-%d %H:%M'),
                'country_name': d['country_name'],
                'organization_name': d['organization_name'],
                'amount': d['donation_amount'],
                'solar_panels': round(d['donation_amount'] / (SOLAR_PANEL_POWER_kW * d['solar_panel_price_per_kw'])),
                'householder': d['householder']
            }
        )

    return render_template("./users/staff/staffdashboard.html", donations=donations)
