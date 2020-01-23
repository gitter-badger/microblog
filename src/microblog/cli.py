from dotenv import find_dotenv, load_dotenv
from flask.cli import FlaskGroup

from . import models
from .app import make_app


def create_app(info):
    return make_app()


cli = FlaskGroup(create_app=create_app)
cli.help = 'Management script for Microblog backend application'


@cli.group(name='db', help='Database related operations')
def db_ops():
    pass


@db_ops.command(name='init', help='Initialize missing database objects')
def db_init():
    models.Author.create_table()
    models.RevokedToken.create_table()
    models.Post.create_table()


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    cli()
