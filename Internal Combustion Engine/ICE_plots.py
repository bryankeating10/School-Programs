import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from engine_calculations import imperical_values

def plots_against_rpm(measurement, imperical_values):
	"""
	Plots the given measurement against RPM for each test condition
	
	Parameters:
	measurement (str): The measurement to plot against RPM.
	imperical_values (dict): Dictionary containing dataframes for each test condition.
	"""
	sns.set_theme(style="darkgrid")  # Use seaborn's whitegrid theme for a professional look
	plt.figure(figsize=(10, 6))
	
	for sheet, data in imperical_values.items():
		sns.lineplot(x=data['RPM'], y=data[measurement], label=sheet, marker='o')  # Use seaborn's lineplot
	
	plt.title(f'{measurement} vs RPM', fontsize=16)
	plt.xlabel('RPM', fontsize=14)
	plt.ylabel(measurement, fontsize=14)
	plt.legend()
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	plt.tight_layout()  # Adjust layout for better spacing

plots_against_rpm('MBP (hp)', imperical_values)
plots_against_rpm('FFR (GPM)', imperical_values)
plots_against_rpm('BSFC (lb/hp-hr)', imperical_values)
plots_against_rpm('BMEP (psi)', imperical_values)
plots_against_rpm('Brake Torque (lb-ft)', imperical_values)
plots_against_rpm('Conv Eff (%)', imperical_values)

plt.show()  # Show all plots at once