from dotenv import find_dotenv, load_dotenv
from flask.cli import FlaskGroup

from .app import make_app
from .models import Post, RevokedToken, Stream, User, db

load_dotenv(find_dotenv())


def create_app(info):
    return make_app()


cli = FlaskGroup(create_app=create_app)
cli.help = 'Management script for Microblog backend application'


@cli.group(name='db')
def db_ops():
    pass


@db_ops.command(name='init')
def db_init():
    db.create_tables([User, Stream, Post, RevokedToken])


if __name__ == '__main__':
    cli()
