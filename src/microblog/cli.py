import click
from werkzeug.serving import run_simple

from .app import application


@click.group()
@click.version_option()
@click.help_option()
def cli():
    pass


@cli.command()
@click.option(
    '-h', '--host', default='127.0.0.1', help='bind to specific network interface'
)
@click.option(
    '-p', '--port', type=int, default=5000, help='listen on specific port number'
)
def run(host, port):
    run_simple(
        host, port, application, use_reloader=True, use_debugger=True,
        reloader_type='watchdog',
    )


if __name__ == '__main__':
    cli()
