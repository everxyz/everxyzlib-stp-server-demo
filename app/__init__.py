from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager


db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = ''
    login_manager.login_message_category = 'info'

    # db.create_all()

    from .main import main
    app.register_blueprint(main, url_prefix='/')

    return app
