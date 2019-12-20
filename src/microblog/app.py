from flask import Flask

from .ext import api, jwt, pony
from .models import RevokedToken
from . import resource


def make_app():
    app = Flask(__name__.split('.')[0])
    app.config['JWT_SECRET_KEY'] = 'very-sekrit'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    configure_extenstions(app)
    return app


def configure_extenstions(app: Flask):
    pony.init_app(app)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_blacklisted(decrypted_token: dict) -> bool:
        jti = decrypted_token['jti']
        return RevokedToken.is_blacklisted(jti)

    configure_api(app)


def configure_api(app: Flask):
    api.add_resource(resource.RegisterResource, '/register')
    api.add_resource(resource.UserLogin, '/login')
    api.add_resource(resource.UserLogoutAccess, '/logout/access')
    api.add_resource(resource.UserLogoutRefresh, '/logout/refresh')
    api.add_resource(resource.TokenRefresh, '/token/refresh')
    api.add_resource(resource.HomeResource, '/recent')
    api.add_resource(
        resource.PostResource, '/post/<string:author_slug>/<string:post_slug>',
    )
    api.add_resource(resource.AuthorResource, '/author/<string:slug>')
    api.init_app(app)
