"""This command checks the code in {tutorial_id}-{lesson_id}.py


E.g. medicode python --tutorial_id tut-4 --lesson_id 1"""

import os
import re
import subprocess
import sys
import time
from pathlib import Path

import click

import medicode_cli.dev_utils as du
from medicode_cli.medicode_api import MedicodeAPI

@click.command()
@click.option("--tutorial_id", required=True, help="The tutorial ID")
@click.option("--lesson_id", required=True, help="The lesson ID")
@click.option("--task_id", required=True, help="The task ID")
def python(tutorial_id: str, lesson_id: str, task_id: str):
    """Run the code in {tutorial_id}-{lesson_id}.py"""

    # Initialize API client
    api = MedicodeAPI()
    # Validate authentication before doing anything else
    api.check_authenticated()

    du.debug_print("Debug mode enabled")

    # Get the absolute path to the student directory
    script_dir = Path(__file__).resolve().parent.parent.parent
    student_dir = script_dir / "student"
    file_path = student_dir / tutorial_id / f"lesson-{lesson_id}.py"

    # Check if the file exists
    if not file_path.exists():
        du.print_error(f"Error: File not found at {file_path}")
        return

    du.debug_print(f"Found student file at: {file_path}")

    # Execute the code in the student file first
    try:
        du.debug_print("Executing student code...")

        result = subprocess.run(
            ["python", str(file_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        print(result.stdout)

        # Show success message
        du.print_success("Code executed successfully!")
    except subprocess.CalledProcessError as e:
        du.print_error(f"Error executing code: {e.stderr}")
        print(e.stdout)  # Print any stdout even if there was an error
    except Exception as e:
        du.print_error(f"Error: {str(e)}")

    # Continue with validation regardless of execution success
    try:
        # Make API request with loading message
        du.print_info("Validating your code...")

        # Read the code file
        with open(file_path) as f:
            student_code = f.read()

        du.debug_print(f"Student code length: {len(student_code)} characters")
        du.debug_print("Making API request to validate code...")

        # Make API request to get the formatted code from the server
        response = api.validate_code(student_code, tutorial_id, lesson_id, task_id)
    
        du.debug_print(f"API response received: {response.keys()}")

        # If the server indicates allow_error is true, we should just pass the student
        if response.get("allow_error"):
            du.print_success("Code validated successfully!")
            return

        # Check if we got code components back (driver code)
        if response.get("success") and response.get("code_components"):
            driver_code = response["code_components"]["driver_code"]
            student_code = response["code_components"]["student_code"]
            
            # Create a combined code string that uses the StudentCodeAnalyzer
            combined_code = du.combine_code(driver_code, student_code)
            du.debug_print(f"Creating combined code with driver code:\n{combined_code}")

            # Run the combined code directly
            try:
                du.print_info("Running tests...")
                
                # Get the path to the medicode_cli directory to make it available in PYTHONPATH
                medicode_cli_dir = Path(__file__).resolve().parent.parent
                
                # Set up environment to make dev_utils available to the subprocess
                env = os.environ.copy()
                # Add the parent directory of medicode_cli to PYTHONPATH so dev_utils can be imported
                if "PYTHONPATH" in env:
                    env["PYTHONPATH"] = f"{medicode_cli_dir.parent}:{env['PYTHONPATH']}"
                else:
                    env["PYTHONPATH"] = str(medicode_cli_dir.parent)
                
                du.debug_print(f"Setting PYTHONPATH: {env.get('PYTHONPATH')}")
                
                # Execute the combined code with the updated environment
                result = subprocess.run(
                    [sys.executable, "-c", combined_code],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    env=env
                )

                if result.returncode == 0:
                    print(result.stdout)
                    du.print_success("✓ Tests passed!")
                else:
                    print(result.stdout)
                    du.debug_print("code has an error")

            except subprocess.TimeoutExpired:
                du.print_error("Test execution timed out. Your code might contain an infinite loop.")
            except Exception as e:  # noqa: BLE001
                du.print_error("Something went wrong")
                du.debug_print(f"Unexpected error running tests: {str(e)}")
        else:
            # If we didn't get required code, display the error message
            du.print_error(f"Error: {response.get('message', 'Unknown error')}")

    except Exception as e:  # noqa: BLE001
        du.print_error("Something went wrong")
        du.debug_print(f"Error during validation: {str(e)}")
