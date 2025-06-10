import click
from ..auth import AuthManager

@click.command()
def logout():
    """Logout from MediCode."""
    auth_manager = AuthManager()
    auth_manager.logout() 