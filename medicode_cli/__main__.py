"""Main entry point for the MediCode CLI."""

import click
from rich.console import Console
from rich.panel import Panel

console = Console()

@click.group()
def cli():
    """MediCode CLI - Student learning environment tools."""
    pass

@cli.command()
def ping():
    """Test connectivity to MediCode services."""
    console.print(Panel("🟢 MediCode CLI is working!", title="Status", border_style="green"))

@cli.command()
def login():
    """Login to MediCode services."""
    console.print(Panel("Login functionality coming soon!", title="Login", border_style="blue"))

@cli.command()
def logout():
    """Logout from MediCode services."""
    console.print(Panel("Logout functionality coming soon!", title="Logout", border_style="blue"))

@cli.command()
def python():
    """Launch Python with MediCode environment."""
    console.print(Panel("Starting Python environment...", title="Python", border_style="yellow"))
    import subprocess
    subprocess.run(["python3"])

if __name__ == "__main__":
    cli() 