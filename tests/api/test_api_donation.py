from flask import url_for
from solar_offset.db import get_db

# TODO add more unit tests


def test_donate_get(app, client):
    with app.app_context():
        response = client.get("/api/donate")
        assert response.status_code == 400
        assert response.text == "No Organization given" or response.text == "No Country code given"

        response = client.get("/api/donate?country=foo")
        assert response.status_code == 400
        assert response.text == "No Organization given"

        response = client.get("/api/donate?orga=bar")
        assert response.status_code == 400
        assert response.text == "No Country code given"

        response = client.get("/api/donate?country=foo&orga=bar")
        assert response.status_code == 400
        assert response.text == "Organization does not exist" or response.text == "Country Code does not exist"

        response = client.get("/api/donate?country=ata&orga=bar")
        assert response.status_code == 400
        assert response.text == "Organization does not exist"

        response = client.get("/api/donate?country=foo&orga=antarctica_solar_project")
        assert response.status_code == 400
        assert response.text == "Country Code does not exist"

        response = client.get("/api/donate?country=ata&orga=antarctica_solar_project")
        assert response.status_code == 200

        response = client.get("/api/donate?country=esp&orga=solaris")
        assert response.status_code == 200

        response = client.get("/api/donate?country=esp&orga=rural_electrification_initiative")
        assert response.status_code == 200

def test_donate_post_not_logged_in(app, client):
    response = client.post("/api/donate", data={})
    assert response.status_code == 401
    assert response.text == "You must be logged in to donate"

def test_donate_post_logged_in(app, client, auth):
    pass