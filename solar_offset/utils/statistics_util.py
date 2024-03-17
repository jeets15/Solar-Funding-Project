# Imports
from solar_offset.db import get_db
from .carbon_offset_util import calculate_reduced_carbon_footprint

# Public Methods

def calculate_statistics():
    return (get_total_users(),
            get_total_countries(),
            get_number_of_donations(),
            get_total_donations(),
            get_reduced_carbon_emissions())


def get_total_users() -> int:
    # Stored Properties
    db = get_db()
    # Fetching all the user from database
    users = db.execute('SELECT * FROM user').fetchall()
    return len(users) or 0


def get_total_countries() -> int:
    # Stored Properties
    db = get_db()
    # Fetching all the countries listed
    countries = db.execute('SELECT * FROM country').fetchall()
    return len(countries) or 0


def get_number_of_donations() -> int:
    # Stored Properties
    db = get_db()
    # Fetching all the donations made
    donations = db.execute('SELECT * FROM donation').fetchall()
    return len(donations) or 0


def get_total_donations() -> int:
    # Stored Properties
    db = get_db()
    # Fetching all the donations made
    donations = db.execute('SELECT * FROM donation').fetchall()
    # Calculate and returns the total donations made
    return sum(int(donation['donation_amount']) for donation in donations) or 0


def get_reduced_carbon_emissions():
    # Calculate the reduced carbon emission based on total donations made
    return calculate_reduced_carbon_footprint(get_total_donations()) or "0 kg"
