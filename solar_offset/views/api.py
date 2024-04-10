from datetime import datetime
from flask import Blueprint, render_template, request, session
from solar_offset.db import get_db
import requests

bp = Blueprint("api", __name__, url_prefix="/api")

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer A21AALeda0KsruBs6n6MJIXdNAB6CBQk4rU41SAFnfFqKZgCP8a7ADGggWtP7YcqZEKYcwoO1GpA7MRcv2hQ4n6MncN7-mXEA"
    # Replace with your PayPal access token
}


@bp.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == 'POST':
        # Ensure that user is logged into a session
        sess_user_id = session.get("user_id", None)
        if sess_user_id is None:
            return "You must be logged in to donate", 401

        # Fetch user record from database
        db = get_db()
        user_entry = db.execute("SELECT * FROM user WHERE user.id == ?", [sess_user_id]).fetchone()

        # Check that the user id exists in the database (could be forged)
        if user_entry is None:
            return "Invalid User Credentials", 400

        # Ensure that the only user role that this user has is 'h' (householder)
        if len(user_entry["user_type"].replace("h", "").replace("_", "")) > 0:
            return "Only Householder accounts are allowed to donate", 403

        # Validate the Form Entries
        data = request.get_json()
        country_code = data.get("country_code")
        order_id = data.get("orderID")

        paypal_order_api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}"
        response = requests.get(paypal_order_api_url, headers=headers)
        paypal_order_data = response.json()
        purchase_units = paypal_order_data.get("purchase_units", [])
        amount_paid = int(round(float(purchase_units[0]["amount"]["value"])))  # Amount paid by the user
        payment_status = paypal_order_data["status"]  # Status of the payment
        if response.status_code != 200:
            return "Failed to retrieve order details from PayPal", 400
        if not purchase_units:
            return "No purchase units found in PayPal order data", 400

        if country_code is None:
            return "You must supply a 'country_code' entry", 400
        country_code = country_code.upper()
        organization_slug = data.get("organization_slug", None)
        if organization_slug is None:
            return "You must supply a 'organization_slug' entry", 400
        organization_slug = organization_slug.lower()
        donation_amount = int(data.get("donation_amount", None))
        if donation_amount is None:
            return "You must supply a 'donation_amount' entry", 400
        if amount_paid != donation_amount or payment_status != "APPROVED":
            return "Payment verification failed", 400
        donation_amount = str(donation_amount)
        if db.execute(
                "SELECT country_code FROM country WHERE country.country_code == ?", [country_code]
        ).fetchone() is None:
            return "Specified Country does not Exist", 400
        if db.execute(
                "SELECT name_slug, country_code FROM organization WHERE name_slug == ? AND country_code == ?",
                [organization_slug, country_code]
        ).fetchone() is None:
            return "Specified Organization does not Exist", 400
        if not donation_amount.isdigit() \
                or int(donation_amount) < 1 \
                or str(int(donation_amount)) != donation_amount:
            return "Donation Amount must be a positive integer", 400
        else:
            donation_amount = int(donation_amount)

        # Insert new Donation into the Database
        timestamp_now = datetime.now()
        db.execute(
            "INSERT INTO donation (created, householder_id, country_code, organization_slug, donation_amount) \
            VALUES (?, ?, ?, ?, ?);",
            [timestamp_now, sess_user_id, country_code, organization_slug, donation_amount]
        )
        db.commit()
        return {"success": True}, 200

    else:
        organization_slug = request.args.get('orga', None)
        country_code = request.args.get('country', None)
        if organization_slug is None:
            return "No Organization given", 400
        elif country_code is None:
            return "No Country code given", 400

        organization_slug = organization_slug.lower()
        country_code = country_code.upper()

        db = get_db()
        country = db.execute("SELECT * FROM country WHERE country_code == ?", [country_code]).fetchone()
        organization = db.execute(
            "SELECT * FROM organization WHERE name_slug == ? AND country_code == ?", [organization_slug, country_code]
        ).fetchone()
        if country is None:
            return "Country Code does not exist", 400
        elif organization is None:
            return "Organization does not exist", 400
        else:
            return render_template(
                "./api/donate.html",
                country=country,
                organization=organization)
