import pandas as pd
from math import sqrt, log as ln, pi
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Read in the engine data to a dictionary of dataframes
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir,'ICE Measured Data.xlsx')
excel_file = pd.ExcelFile(file_path)
tests = {'One-Quarter Throttle': None, 'One-Half Throttle': None, 
         'Three-Quarter Throttle': None, 'Full Throttle': None}
for sheet_name in excel_file.sheet_names:
    tests[sheet_name] = pd.read_excel(file_path, sheet_name=sheet_name)

# Displays the first column and last 10 columns of each dataframe
def display_df(tests):
	for sheet_name, df in tests.items():
		print(sheet_name)
		print(df.iloc[:, [0]].join(df.iloc[:, -10:]))

# Engine constants
connecting_rod_length = 0.105  # m
engine_displacement = 163e-6  # m^3
bore_diameter = 0.068  # m
stroke_length = 0.045  # m
n_p = 2 # Revolutions per power stroke


# Fuel constants
density = 750  # kg/m^3

# Measured Brake power (MBP) calculation in Watts
eta = 0.8  # Efficiency of the engine
for test in tests.values():
	test['MBP (W)'] = test['Oil Pressure (Pa)'] * test['Oil Flow Rate (m^3/s)']* eta

# Fuel flow rate (FFR) calculation in m^3/s
for test in tests.values():
	test['FFR (m^3/s)'] = test['Difference (kg)'] / test['Run Time (s)']

# Brake specific fuel consumption (BSFC) calculation in kg/Nm
for test in tests.values():
	test['BSFC (kg/Nm)'] = test['FFR (m^3/s)'] / test['MBP (W)']

# Rev time calculation in seconds
for test in tests.values():
	test['Rev Time (s)'] = 1 / test['RPM']

# Brake mean effective pressure (BMEP) calculation in Pa
for test in tests.values():
	test['BMEP (Pa)'] = test['MBP (W)'] * n_p / (engine_displacement * test['Rev Time (s)'])

# Brake torque calculation in Nm
for test in tests.values():
	test['Brake Torque (Nm)'] = test['MBP (W)'] / (2 * pi * test['RPM'])




display_df(tests)
