from flask import session, url_for
from solar_offset.db import get_db
import json


# TODO add more unit tests


def test_donate_get(client):
    res = client.get("/api/donate")
    assert res.status_code == 400
    assert res.text == "No Organization given" or res.text == "No Country code given"

    res = client.get("/api/donate?country=foo")
    assert res.status_code == 400
    assert res.text == "No Organization given"

    res = client.get("/api/donate?orga=bar")
    assert res.status_code == 400
    assert res.text == "No Country code given"

    res = client.get("/api/donate?country=foo&orga=bar")
    assert res.status_code == 400
    assert res.text == "Organization does not exist" or res.text == "Country Code does not exist"

    res = client.get("/api/donate?country=ata&orga=bar")
    assert res.status_code == 400
    assert res.text == "Organization does not exist"

    res = client.get("/api/donate?country=foo&orga=antarctica_solar_project")
    assert res.status_code == 400
    assert res.text == "Country Code does not exist"

    res = client.get("/api/donate?country=ata&orga=antarctica_solar_project")
    assert res.status_code == 200

    res = client.get("/api/donate?country=esp&orga=solaris")
    assert res.status_code == 200

    res = client.get("/api/donate?country=esp&orga=rural_electrification_initiative")
    assert res.status_code == 200


def test_donate_post_not_logged_in(client):
    headers = {'Content-Type': 'application/json'}
    res = client.post("/api/donate", data=json.dumps({}), headers=headers)
    assert res.status_code == 401
    assert res.text == "You must be logged in to donate"


def test_donate_post_modified_user_session(client):
    with client.session_transaction() as session:
        session['user_id'] = '123456789'
    headers = {'Content-Type': 'application/json'}
    res = client.post("/api/donate", data=json.dumps({}), headers=headers)
    assert (res.status_code, res.text) == (400, "Invalid User Credentials")


def test_donate_post_logged_in_non_householder(client, auth):
    with client:
        auth.login(username="staff3881@hhrs", password="staff@29r83910")
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json.dumps({}), headers=headers)
        assert (res.status_code, res.text) == (403, "Only Householder accounts are allowed to donate")

    with client:
        auth.login(username="admin1@12", password="admin$219047")
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json.dumps({}), headers=headers)
        assert (res.status_code, res.text) == (403, "Only Householder accounts are allowed to donate")

    with client:
        auth.login(username="staffmin12", password="staffmin12")
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json.dumps({}), headers=headers)
        assert (res.status_code, res.text) == (403, "Only Householder accounts are allowed to donate")


def test_donate_post_logged_in_householder_no_data(client, auth):
    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json.dumps({}), headers=headers)
        assert (res.status_code, res.text) == (400, "You must supply a 'country_code' entry") \
               or (res.status_code, res.text) == (400, "You must supply a 'organization_slug' entry") \
               or (res.status_code, res.text) == (400, "You must supply a 'donation_amount' entry")


def test_donate_post_logged_in_householder_single_data(client, auth):
    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "country_code": "foo"
        }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "You must supply a 'organization_slug' entry") \
               or (res.status_code, res.text) == (400, "You must supply a 'donation_amount' entry")

    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "organization_slug": "bar"
        }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "You must supply a 'country_code' entry") \
               or (res.status_code, res.text) == (400, "You must supply a 'donation_amount' entry")

    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "donation_amount": "NaN"
        }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "You must supply a 'country_code' entry") \
               or (res.status_code, res.text) == (400, "You must supply a 'organization_slug' entry")


def test_donate_post_logged_in_householder_data_pairs(client, auth):
    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "country_code": "foo",
            "organization_slug": "bar"
        }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "You must supply a 'donation_amount' entry")

    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "country_code": "foo", "donation_amount": "NaN"
        }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "You must supply a 'organization_slug' entry")

    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "organization_slug": "bar", "donation_amount": "NaN"
        }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "You must supply a 'country_code' entry")


def test_donate_post_logged_in_householder_full_data(client, auth):
    cases = [
        (
            {"country_code": "foo", "organization_slug": "bar", "donation_amount": "NaN"},
            [(400, "Specified Country does not Exist"), (400, "Specified Organization does not Exist"),
             (400, "Donation Amount must be a positive integer")]
        ),
        (
            {"country_code": "ata", "organization_slug": "bar", "donation_amount": "NaN"},
            [(400, "Specified Organization does not Exist"), (400, "Donation Amount must be a positive integer")]
        ),
        (
            {"country_code": "foo", "organization_slug": "antarctica_solar_project", "donation_amount": "NaN"},
            [(400, "Specified Country does not Exist"), (400, "Donation Amount must be a positive integer")]
        ),
        (
            {"country_code": "foo", "organization_slug": "bar", "donation_amount": "1"},
            [(400, "Specified Country does not Exist"), (400, "Specified Organization does not Exist")]
        ),
        (
            {"country_code": "ata", "organization_slug": "antarctica_solar_project", "donation_amount": "NaN"},
            [(400, "Donation Amount must be a positive integer")]
        ),
        (
            {"country_code": "ata", "organization_slug": "bar", "donation_amount": "1"},
            [(400, "Specified Organization does not Exist")]
        ),
        (
            {"country_code": "foo", "organization_slug": "antarctica_solar_project", "donation_amount": "1"},
            [(400, "Specified Country does not Exist")]
        ),
        (
            {"country_code": "ata", "organization_slug": "antarctica_solar_project", "donation_amount": "1"},
            [(200, '{"success":true}\n')]
        )
    ]
    for post_data, assertions in cases:
        with client:
            auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
            res = client.post("/api/donate", data=json.dumps(post_data), content_type="application/json")
            print((res.status_code, res.text))
            print(assertions)
            assert any([(res.status_code, res.text) == a for a in assertions])


def test_donate_post_donation_amount(client, auth):
    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "country_code": "ata",
            "organization_slug": "antarctica_solar_project",
            "donation_amount": "1.1"
        }
        json_data = json.dumps(data)

        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "Donation Amount must be a positive integer")

    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "country_code": "ata",
            "organization_slug": "antarctica_solar_project",
            "donation_amount": "0"
        }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "Donation Amount must be a positive integer")

    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "country_code": "ata",
            "organization_slug": "antarctica_solar_project",
            "donation_amount": "0.5"
        }
        json_data = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "Donation Amount must be a positive integer")

    with client:
        auth.login(username="jane.doe15@example.com", password="12Jane!DoeDoe")
        data = {
            "country_code": "ata",
            "organization_slug": "antarctica_solar_project",
            "donation_amount": "-1"
        }
        json_data = json.dumps(data)
        res = client.post("/api/donate", data=json_data, headers=headers)
        assert (res.status_code, res.text) == (400, "Donation Amount must be a positive integer")
