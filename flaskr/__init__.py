import os
from flask import (Flask, g)
from flask import render_template
from flaskr.db import get_db
import time

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        DATABASE=os.path.join(app.instance_path, 'myCryptoBotDB.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import coinmarketcapAPI_test
    app.register_blueprint(coinmarketcapAPI_test.bp)

    from . import telegram_notifier
    app.register_blueprint(telegram_notifier.bp)

    @app.route('/')
    def hello():
        g.data = get_db().execute(
            'SELECT * FROM responces')
        return render_template('home.html')

    from . import coinmarketcap_api
    app.register_blueprint(coinmarketcap_api.bp)

    return app