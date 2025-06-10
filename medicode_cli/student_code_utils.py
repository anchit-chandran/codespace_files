"""Utils used in the driver development tool for the Medicode webapp."""

# ~~~START CONFIG~~~
import ast
import io
import json
import os
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

from dev_utils import debug_print, DEBUG

# ~~~END CONFIG~~~



def run_student_code(student_code_path: str, timeout: int = 5, ):
    """Execute student code as a subprocess and analyze using AST"""
    debug_print(f"Starting run_student_code with file: {student_code_path}")
    start_time = time.time()

    # Path to student code
    student_file = Path(student_code_path)
    debug_print(f"Student file path: {student_file.absolute()}")
    
    if not student_file.exists():
        debug_print(f"ERROR: Student file does not exist: {student_file.absolute()}")
        return {
            "success": False,
            "stdout": "",
            "stderr": f"File not found: {student_file.absolute()}",
            "variables": {},
        }

    # Extract the student code section from the combined file
    combined_content = student_file.read_text()
    debug_print(f"File size: {len(combined_content)} bytes")
    
    # Extract student code portion (between # <STUDENT_CODE> and # </STUDENT_CODE>)
    student_code_match = re.search(r"# <STUDENT_CODE>\n(.*?)\n# </STUDENT_CODE>", 
                                  combined_content, re.DOTALL)
    
    if student_code_match:
        student_code = student_code_match.group(1)
        debug_print(f"Extracted student code portion: {len(student_code)} bytes")
    else:
        student_code = combined_content
        debug_print("Could not find student code markers, using entire file")

    # Run the student code as a subprocess
    try:
        debug_print(f"Executing student code with subprocess: {student_file}")
        result = subprocess.run(
            ["python", str(student_file)],
            capture_output=True,
            text=True,
            timeout=5  # Add a timeout to prevent infinite loops
        )
        
        stdout = result.stdout
        stderr = result.stderr
        
        # Parse the student code using AST to extract defined variables
        debug_print("Parsing student code with AST")
        parsed_ast = ast.parse(student_code)
        
        # Extract top-level variables and their types
        variables = {}
        for node in parsed_ast.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id
                        # We can only identify the variable name, not its value with static AST
                        variables[var_name] = {"type": "unknown"}
        
        debug_print(f"Execution completed in {time.time() - start_time:.2f} seconds")
        
        return {
            "success": result.returncode == 0,
            "stdout": stdout.strip(),
            "stderr": stderr,
            "variables": variables,
            "student_code": student_code,
        }
    except subprocess.TimeoutExpired:
        debug_print("Subprocess timed out")
        return {
            "success": False,
            "stdout": "",
            "stderr": "Execution timed out. Your code may contain an infinite loop.",
            "variables": {},
            "student_code": student_code,
        }
    except Exception as e:
        debug_print(f"Exception during execution: {type(e).__name__}: {str(e)}")
        debug_print(traceback.format_exc())
        
        return {
            "success": False,
            "stdout": "",
            "stderr": traceback.format_exc(),
            "variables": {},
            "student_code": student_code,
        }


def check_std_has_expected_output(std: str, expected_output: str, error_message: str) -> bool:
    """Check if the stderr or stdout contains the expected output"""
    if DEBUG:
        debug_print(f"Checking if '{expected_output}' is in '{std}'")
    match = re.search(expected_output, std) is not None
    if DEBUG:
        debug_print(f"Match result: {match}")
    assert match, error_message


def check_student_code_has_pattern(student_code: str, pattern: str, error_message: str) -> bool:
    """Check if the student_code contains the pattern"""
    if DEBUG:
        debug_print(f"Checking if pattern '{pattern}' exists in student code")
    match = re.search(pattern, student_code) is not None
    if DEBUG:
        debug_print(f"Match result: {match}")
    assert match, error_message
