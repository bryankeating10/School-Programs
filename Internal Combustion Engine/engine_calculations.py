import pandas as pd
from math import sqrt, log as ln, pi
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Read in the temperature data
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir,'Mark Formatted Test Data.xlsx')
tests = {'Test 1 - High MFR Low Crnt': None, 'Test 2 - High MFR High Crnt': None, 
         'Test 3 - Low MFR High Crnt': None, 'Test 4 - Low MFR Low Crnt': None}
tests_temps = tests.copy()

for sheet_name, test in zip(excel_file.sheet_names, tests):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    tests[test] = df
