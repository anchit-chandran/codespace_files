# Example driver code for the task:
# "Print out 23 + 40 x 8. You should get 343."

# NOTE: This code will be indented and wrapped in a function by combine_code
# Do not include any try/except blocks or indentation handling

# Check if the code contains the correct calculation pattern
analyzer.check_student_code_has_pattern(
    r"print\s*\(\s*23\s*\+\s*40\s*\*\s*8\s*\)", 
    "Your code should print 23 + 40 * 8"
)

# Check if the output is correct (343)
analyzer.check_std_has_expected_output(
    r"343", 
    "The output should be 343. Remember that * has precedence over +"
)

# This will only run if all checks pass
print("Great job! Your calculation is correct.") 