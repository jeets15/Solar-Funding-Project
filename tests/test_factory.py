from solar_offset import create_app
from solar_offset.db import get_db

## Test the app creation factory function

# By default, the app should not be in testing mode
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_config_auth(app, client, auth):
    account_user_id = None
    with app.app_context():
        account_user_id = get_db().execute(
            "SELECT id FROM user WHERE email_username == ?",
            ["admin1@12"]
            ).fetchone()['id']
    assert account_user_id is not None
    with client:
        auth.login(username="admin1@12", password="admin$219047")
        with client.session_transaction() as session:
            assert account_user_id == session.get('user_id')
        
        auth.logout()
        with client.session_transaction() as session:
            assert 'user_id' not in session