import os
import tempfile

import pytest
from solar_offset import create_app
from solar_offset.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # Create test database as temporary file
    db_fd, db_path = tempfile.mkstemp()

    # Define testing configuration
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Populate database with test data
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()