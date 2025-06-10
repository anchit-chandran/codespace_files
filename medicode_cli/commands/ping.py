import click

from medicode_cli.medicode_api import MedicodeAPI


@click.command()
def ping():
    """Health check ping"""

    api = MedicodeAPI()

    api.health_check()
    
