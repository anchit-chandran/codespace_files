# Example driver code for a more complex task:
# "Create a list of patient blood pressures and calculate the average."

# NOTE: This code will be indented and wrapped in a function by combine_code
# Do not include any try/except blocks or indentation handling

# Check that they defined a list of blood pressures
analyzer.check_variable_exists(
    "blood_pressures", 
    "You need to create a list variable named 'blood_pressures'"
)

# Check that blood_pressures is actually a list
if not isinstance(analyzer.execution_vars["blood_pressures"], list):
    raise AssertionError("blood_pressures should be a list")

# Check that they calculated the average correctly
analyzer.check_variable_exists(
    "average_bp", 
    "You need to create a variable named 'average_bp' to store the average"
)

# Calculate the expected average manually
expected_avg = sum(analyzer.execution_vars["blood_pressures"]) / len(analyzer.execution_vars["blood_pressures"])

# Allow some floating point difference
import math
actual_avg = analyzer.execution_vars["average_bp"]
if math.isclose(actual_avg, expected_avg, rel_tol=1e-6):
    print(f"Great job! You correctly calculated the average as {actual_avg}")
else:
    raise AssertionError(f"Your average ({actual_avg}) doesn't match the expected value ({expected_avg})")

# Check that they printed the result
analyzer.check_std_has_expected_output(
    r"average\s*(blood\s*pressure|bp).*?[\d\.]+", 
    "You should print the average blood pressure with a descriptive message"
) 