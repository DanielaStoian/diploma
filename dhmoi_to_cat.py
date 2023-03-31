import pandas as pd
import numpy as np

data = pd.read_csv('dhmoi_cat.csv')
cat = []
charact_column = data.columns[1]
for char in data[charact_column]:
    if char == "Μεσαίες Περιοχές Λοιπής Ελλάδας":
        cat.append(3)
    elif char == "Πολεοδομικό συγκρότημα Αθήνας" or char == 'Πολεοδομικό Συγκρότημα Αθήνας':   
        cat.append(1)
    elif char == "Απομακρυσμένες Περιοχές & Μικρά Νησιά":   
        cat.append(3)        
    elif char == "Δήμοι >30.000 κατοίκους":   
        cat.append(2)
    elif char == "Λοιπές Πρωτεύουσες Νομών":   
        cat.append(2)
    elif char == "20 Μεγάλες Πόλεις":   
        cat.append(1)
    elif char == "Πολεοδομικό Συγκρότημα Θεσσαλονίκης":   
        cat.append(1)
data['category'] = cat        
data.to_csv("organized_dhmoi.csv")

