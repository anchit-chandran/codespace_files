# Fix this poorly written PE triage code
clinical_suspicion = input('What is the clinical probability of a PE (low/high): ')

print('Perform D-dimer.')
ddimer_positive = input('Is the D-Dimer positive (y/n): ')

if (clinical_suspicion == 'low') and (ddimer_positive == 'y'):
    print('Patient requires CTPA')

if (clinical_suspicion == 'low') and (ddimer_positive == 'n'):
    print('Explore other causes of symptoms')
        
else:
    print('Patient requires CTPA')