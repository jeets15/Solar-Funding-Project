import os
from flask import Flask, url_for

# `python -m flask --app solar_offset run --port 8000 --debug` to run the development server

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'solar_offset.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    from .views import householder, admin, staff, api
    app.register_blueprint(householder.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(staff.bp)
    app.register_blueprint(api.bp)

    return app
