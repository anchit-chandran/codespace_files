```python
from IPython.display import clear_output

# fill in patient1_data
data = {
    'first_name': '',  # STRING
    'last_name': '',   # STRING
    'dob': 'DD/MM/YYYY',
    'obs': {
        'hr': []       # LIST of INT heart rates
    }
}

all_patients = { 'patient1': data }
commands = ['add obs', 'delete', 'exit']

while True:
    # print commands and prompt for user input
    # clear_output() where appropriate
    # implement add obs, delete and exit per guided steps
    pass
```