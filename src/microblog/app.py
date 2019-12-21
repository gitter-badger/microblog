from flask import Flask

from .ext import api, pony


def make_app():
    app = Flask(__name__.split('.')[0])
    configure_extenstions(app)
    return app


def configure_extenstions(app: Flask):
    pony.init_app(app)
    configure_resources()
    api.init_app(app)


def configure_resources():
    from . import resource  # noqa: F401
