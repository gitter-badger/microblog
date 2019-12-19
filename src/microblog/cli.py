from dotenv import find_dotenv, load_dotenv
from flask.cli import FlaskGroup

from .app import make_app


def create_app(info):
    return make_app()


cli = FlaskGroup(create_app=create_app)
cli.help = 'Management script for Microblog backend application'


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    cli()
