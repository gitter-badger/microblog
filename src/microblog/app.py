import os

from flask import Flask

from .ext import api, jwt, pony
from .models import RevokedToken


def make_app():
    app = Flask(__name__.split('.')[0])
    configure_app(app)
    configure_extenstions(app)
    return app


def configure_app(app: Flask):
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedToken.is_blacklisted(jti)


def configure_extenstions(app: Flask):
    pony.init_app(app)
    configure_resources()
    api.init_app(app)
    jwt.init_app(app)


def configure_resources():
    from . import resource  # noqa: F401
