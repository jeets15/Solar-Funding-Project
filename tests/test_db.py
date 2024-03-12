import sqlite3
import pytest
from solar_offset.db import get_db

def test_get_close_db(app):
    # Database get opened in with statement
    # and should be automatically closed
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # The database should be closed again here
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    # Replace init_db function with fake one
    # to test whether this function is actually called with the command
    monkeypatch.setattr('solar_offset.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called