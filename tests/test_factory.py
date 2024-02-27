from solar_offset import create_app

## Test the app creation factory function

# By default, the app should not be in testing mode
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing