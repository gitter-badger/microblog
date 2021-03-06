import os
from datetime import timedelta

from flask import Flask

from .ext import api, jwt
from .models import RevokedToken, User, db


def make_app():
    app = Flask(__name__.split('.')[0])
    configure_app(app)
    configure_extenstions(app)
    return app


def configure_app(app: Flask):
    app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30*6)
    app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedToken.is_blacklisted(jti)

    @jwt.user_loader_callback_loader
    def load_user(identity):
        return User.get_or_none(User.id == identity)

    @app.before_request
    def db_connect():
        db.connect()

    @app.teardown_request
    def db_close(exc):
        if not db.is_closed():
            db.close()


def configure_extenstions(app: Flask):
    db.init(
        os.environ['DB_FILENAME'],
        pragmas={
            'journal_mode': 'wal',
            'cache_size': -1 * 64000,  # 64MB
            'foreign_keys': 1,
            'ignore_check_constraints': 0,
            'synchronous': 0
        }
    )
    configure_resources()
    api.init_app(app)
    jwt.init_app(app)


def configure_resources():
    from . import resource  # noqa: F401
