import os
from flask import Flask
import pyrebase


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', default='dev')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Firebase Configuration
    firebase = pyrebase.initialize_app(app.config['CONFIG'])
    app.firebase = firebase
    app.db = firebase.database()

    # Import and register your Flask routes/views here
    from . import routes
    app.register_blueprint(routes.bp)

    return app
