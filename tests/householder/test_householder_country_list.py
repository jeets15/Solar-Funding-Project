
import json

from solar_offset.db import get_db


# TODO add more test cases
def test_countries(app, client):

    with app.app_context():
        db = get_db()

        response = client.get("/countries?raw")
        r_json = json.loads(response.data)

        # Ensure that these fields are not contained in the 'raw' response
        if len(r_json) > 0:
            assert "description" not in r_json[0]
            assert "electricty_consumption" not in r_json[0]
            assert "short_code" not in r_json[0]

        count_countries = db.execute("SELECT COUNT(country_code) AS code_count \
                                     FROM country;").fetchone()["code_count"]
        assert count_countries == len(r_json)


def test_countries_donation_sums(app, client):
    with app.app_context():
        response = client.get("/countries?raw")
        r_json = json.loads(response.data)

        db = get_db()
        donations = db.execute("SELECT * FROM donation").fetchall()
        print([ dict(d) for d in donations ])

        for country_json in r_json:
            print(f"Country: {country_json['country_code']}")
            country_donations = [ d['donation_amount'] for d in donations if str(d['country_code']) == str(country_json['country_code']) ]

            print(f"Donation Stats in Country List Page: count={country_json['donation_count']}, total={country_json['donation_sum']}")
            print(f"Manually Summed Donations:           count={len(country_donations)}, total={sum(country_donations)}")

            assert country_json['donation_count'] == len(country_donations)
            assert country_json['donation_sum'] == sum(country_donations)