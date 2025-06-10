# START PRIOR CODE
import sys
import os

# Add the parent directory to sys.path
sys.path.append("..")
# Add the current directory's parent to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

STUDENT_CODE = """print(39-50+12*39/(5*4))"""

from medicode_cli.student_code_utils import StudentCodeAnalyzer

analyzer = StudentCodeAnalyzer(STUDENT_CODE)
# END PRIOR CODE

result = analyzer.run_code()

analyzer.check_stdout_matches_pattern(r"-10.2512", "You should be printing out `-10.2512`")
