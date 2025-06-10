# Enable/disable debug mode
import os
import sys

from rich.console import Console

DEBUG = os.environ.get("MEDICODE_DEBUG", "0") == "1"

console = Console()

def debug_print(message):
    """Print a debug message if debug mode is enabled"""
    if DEBUG:
        console.print(f"[DEBUG:UTILS] {message}", file=sys.stderr)

def print_success(message):
    """Print a success message"""
    console.print(f"[green]✅ {message}[/green]", file=sys.stderr)

def print_error(message):
    """Print an error message"""
    console.print(f"[red]❌ {message}[/red]", file=sys.stderr)

def print_info(message):
    """Print an info message"""
    console.print(f"[cyan]🔎 {message}[/cyan]", file=sys.stderr)

def combine_code(driver_code: str) -> str:
    """Combine the utils code and driver code into a single file that will import student code"""
    # Read the student_code_utils.py content
    utils_path = os.path.join(os.path.dirname(__file__), "student_code_utils.py")
    with open(utils_path) as f:
        utils_code = f.read()
    
    # Combine utils and driver code, with student code being imported
    return f"""# Import student code as a module
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import student_code

{utils_code}

{driver_code}"""