from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from .main import main


db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    app.register_blueprint(main, url_prefix='/')

    return app
