import click
from rich.console import Console
from ..auth import AuthManager

console = Console()

@click.command()
def login():
    """Login to MediCode."""
    console.print("[bold blue]Welcome to MediCode![/bold blue]")
    console.print("\nA browser window will open for you to login securely.")
    console.print("Your login session will be saved locally and used for all MediCode commands.")
    console.print("[yellow]For security reasons, never share your ~/.medicode directory with others.[/yellow]\n")
    
    auth_manager = AuthManager()
    auth_manager.login()
    
    console.print("\n[green]You're all set![/green] You can now use other MediCode commands.")
    