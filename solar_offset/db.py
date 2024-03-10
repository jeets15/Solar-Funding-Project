import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def db_executescript(f):
    db = get_db()
    db.executescript(f.read())

@click.command('init-db')
@click.argument("files", nargs=-1, type=click.File('r'))
# @click.option('-f', '--file', 'population_script', default=None, type=click.File('r'))
def init_db_command(files):
    """Clear the existing data and create new tables."""
    """Optionally, execute a population script to populate the database table with records."""
    init_db()
    click.echo('Initialized the database.')
    if files:
        click.echo('Executing sql scripts...')
        for f in files:
            db_executescript(f)
        click.echo('Success.')




# Register with the App
def init_app(app):
    # Closes database every time that a request is cleaned up
    app.teardown_appcontext(close_db)

    # adds a new command that can be called with the flask command to initialize a database
    app.cli.add_command(init_db_command)