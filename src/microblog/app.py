from flask import Flask

from .ext import api, jwt, pony
from .models import RevokedToken


def make_app():
    app = Flask(__name__.split('.')[0])
    app.config['JWT_SECRET_KEY'] = 'very-sekrit'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    configure_extenstions(app)
    configure_resources()
    return app


def configure_extenstions(app: Flask):
    pony.init_app(app)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_blacklisted(decrypted_token: dict) -> bool:
        jti = decrypted_token['jti']
        return RevokedToken.is_blacklisted(jti)

    api.init_app(app)


def configure_resources():
    from . import resource  # noqa: F401
