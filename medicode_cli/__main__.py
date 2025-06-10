import click

from medicode_cli.commands import login, logout, ping, python


@click.group()
def cli():
    """MediCode CLI - A command-line interface for MediCode."""
    pass


# Register commands
cli.add_command(login.login, name="login")
cli.add_command(logout.logout, name="logout")
cli.add_command(python.python, name="python")
cli.add_command(ping.ping, name="ping")

if __name__ == "__main__":
    cli() 