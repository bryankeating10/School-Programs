import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from engine_calculations import imperical_values

def plots_against_rpm(measurement, imperical_values):
	"""
	Plots the given measurement against RPM for each test condition with filled circles at each data point.
	
	Parameters:
	measurement (str): The measurement to plot against RPM.
	imperical_values (dict): Dictionary containing dataframes for each test condition.
	"""
	plt.figure(figsize=(10, 6))
	for sheet, data in imperical_values.items():
		plt.plot(data['RPM'], data[measurement], label=sheet, marker='o')  # Add marker='o' for filled circles
	
	plt.title(f'{measurement} vs RPM')
	plt.xlabel('RPM')
	plt.ylabel(measurement)
	plt.legend()
	plt.grid()
	plt.show()

plots_against_rpm('MBP (hp)', imperical_values)
plots_against_rpm('FFR (GPM)', imperical_values)
plots_against_rpm('BSFC (lb/hp-hr)', imperical_values)
plots_against_rpm('BMEP (psi)', imperical_values)
plots_against_rpm('Brake Torque (lb-ft)', imperical_values)
plots_against_rpm('Conv Eff (%)', imperical_values)