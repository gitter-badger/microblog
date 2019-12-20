from flask import Flask

from .ext import api, pony
from . import resource


def make_app():
    app = Flask(__name__.split('.')[0])
    configure_extenstions(app)
    return app


def configure_extenstions(app: Flask):
    pony.init_app(app)
    configure_api(app)


def configure_api(app: Flask):
    api.add_resource(resource.HomeResource, '/recent')
    api.add_resource(
        resource.PostResource, '/post/<string:author_slug>/<string:post_slug>',
    )
    api.add_resource(resource.AuthorResource, '/author/<string:slug>')
    api.add_resource(resource.Register, '/register')
    api.init_app(app)
