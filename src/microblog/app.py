import os

from flask import Flask

from .ext import api, jwt
from .models import RevokedToken, db


def make_app():
    app = Flask(__name__.split('.')[0])
    configure_app(app)
    configure_extenstions(app)
    return app


def configure_app(app: Flask):
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedToken.is_blacklisted(jti)

    @app.before_request
    def db_connect():
        db.connect()

    @app.teardown_request
    def db_close(exc):
        if not db.is_closed():
            db.close()


def configure_extenstions(app: Flask):
    configure_resources()
    api.init_app(app)
    jwt.init_app(app)


def configure_resources():
    from . import resource  # noqa: F401
