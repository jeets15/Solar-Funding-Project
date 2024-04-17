from collections import namedtuple
from datetime import datetime
from flask import Blueprint, render_template, request, session
from solar_offset.db import get_db
import requests
from dotenv import load_dotenv
import os
import subprocess

from solar_offset.utils.carbon_offset_util import SOLAR_PANEL_POWER_kW

load_dotenv()


def get_paypal_access_token():
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")
    token_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(token_url, headers=headers, auth=(client_id, client_secret), data=data)

    if response.status_code == 200:
        # Extract the access token from the response
        access_token = response.json().get("access_token")
        return access_token
    else:
        # Handle error case
        print("Error occurred while retrieving access token:", response.text)
        return None


def verify_paypal_order(order_id, donation_amount):
    PaypalVerification = namedtuple("PaypalVerification", ['valid', 'error_message'])

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + PAYPAL_ACCESS_TOKEN
    }
    req_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}"

    response = requests.get(req_url, headers=headers)

    if response.status_code != 200:
        return PaypalVerification(False, "Failed to retrieve order details from PayPal")

    paypal_order_data = response.json()
    purchase_units = paypal_order_data.get("purchase_units", [])
    amount_paid = int(round(float(purchase_units[0]["amount"]["value"])))  # Amount paid by the user
    payment_status = paypal_order_data["status"]
    if amount_paid != donation_amount or payment_status != "APPROVED":
        return PaypalVerification(False, "Payment verification failed")

    # Successful verification
    return PaypalVerification(True, None)


PAYPAL_ACCESS_TOKEN = get_paypal_access_token()
bp = Blueprint("api", __name__, url_prefix="/api")

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + PAYPAL_ACCESS_TOKEN
}


@bp.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == 'POST':
        # Ensure that user is logged into a session
        sess_user_id = session.get("user_id", None)
        print("Paypal access token", PAYPAL_ACCESS_TOKEN)
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
        donation_amount = data.get("donation_amount", None)
        order_id = data.get("orderID")

        if donation_amount is None:
            return "You must supply a 'donation_amount' entry", 400
        if country_code is None:
            return "You must supply a 'country_code' entry", 400
        country_code = country_code.upper()
        organization_slug = data.get("organization_slug", None)
        if organization_slug is None:
            return "You must supply a 'organization_slug' entry", 400
        organization_slug = organization_slug.lower()
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

            # Verify that form data is supported by paypal API info
        verification = verify_paypal_order(order_id, donation_amount)
        if not verification.valid:
            return verification.error_message, 400

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
        print("Organization: ",organization_slug)
        print("Country code: ",country_code)
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
            solarprice = country["solar_panel_price_per_kw"] * SOLAR_PANEL_POWER_kW
            return render_template(
                "./api/donate.html",
                solarprice=solarprice,
                country=country,
                organization=organization)
