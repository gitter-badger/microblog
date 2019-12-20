from flask import Flask

from .ext import pony
from .api import api_bp


def make_app():
    app = Flask(__name__.split('.')[0])
    configure_extenstions(app)
    configure_blueprints(app)
    return app


def configure_extenstions(app: Flask):
    pony.init_app(app)


def configure_blueprints(app: Flask):
    app.register_blueprint(api_bp)
