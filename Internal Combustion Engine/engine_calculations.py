import pandas as pd
from math import sqrt, log as ln, pi
import os
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl.styles import Alignment

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
hhv = 47.3e6  # J/kg (higher heating value of gasoline)
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

# Conversion efficiency (Conv Eff) calculation in %
for test in tests.values():
	test['Conv Eff (%)'] = (test['MBP (W)'] * 100) / (test['FFR (m^3/s)'] * hhv)

# Write the data to a results Excel file
output_file_path = os.path.join(current_dir, 'Engine Calculations.xlsx')
with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
	for sheet_name, df in tests.items():
		df.to_excel(writer, sheet_name=sheet_name, index=False)
		worksheet = writer.sheets[sheet_name]
		for col_idx, col in enumerate(df.columns, start=1):
			column_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
			worksheet.column_dimensions[worksheet.cell(row=1, column=col_idx).column_letter].width = column_width
		# Center align all cells
		for row in worksheet.iter_rows(min_row=1, max_row=worksheet.max_row, min_col=1, max_col=worksheet.max_column):
			for cell in row:
				cell.alignment = Alignment(horizontal='center', vertical='center')

# Open the results Excel file
os.startfile(output_file_path)


display_df(tests)
