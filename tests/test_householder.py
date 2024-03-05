
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