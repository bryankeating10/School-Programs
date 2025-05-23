import pandas as pd
from math import sqrt, log as ln, pi
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Read in the temperature data
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir,'Formatted Test Data.xlsx')
excel_file = pd.ExcelFile(file_path)
tests = {'Test 1 - High MFR Low Crnt': None, 'Test 2 - High MFR High Crnt': None, 
         'Test 3 - Low MFR High Crnt': None, 'Test 4 - Low MFR Low Crnt': None}
tests_temps = tests.copy()

for sheet_name, test in zip(excel_file.sheet_names, tests):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    tests[test] = df

# Read in the measured data
file_path = os.path.join(current_dir,'Measured Data.xlsx')
excel_file = pd.ExcelFile(file_path)
measured_data = pd.read_excel(file_path)

# Calculate mass flow rate
water_density = 997.77 # kg/m^3
specific_gas_constant = 287.058 # J/kgK
orifice_area = 0.001265 # m^2
flow_coefficient = 0.6

measured_data['Air Pressure'] = None
measured_data['Air Density'] = None
measured_data['Mass Flow Rate'] = None

for index, exp in measured_data.iterrows():		# Calculates the air pressure
	measured_data.loc[index, 'Air Pressure'] = water_density * 9.81 * exp['Fan Mano'] + 101325
for index, exp in measured_data.iterrows():		# Calculates the air density
	measured_data.loc[index, 'Air Density'] = exp['Air Pressure'] / (specific_gas_constant * exp['Inlet Temp'])
for index, exp in measured_data.iterrows():
	temp_var = sqrt((2*9.81*water_density*((exp['Fan Mano'] - exp['Orifice Mano'])) / measured_data['Air Density'][index]))
	measured_data.loc[index, 'Mass Flow Rate'] = temp_var * measured_data['Air Density'][index]*orifice_area*flow_coefficient

# Calculate heat generation
d_i = 0.03261 # Pipe diameter (m)
d_0 = 0.05326 # Insulation outer diameter (m)
area_pipe = pi*(d_i**2)/4 # Pipe cross-sectional area (m^2)
pipe_length = 1.7526 # (m)

measured_data['Power'] = None
measured_data['Heat Generation'] = None

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Power'] = exp['Voltage'] * exp['Current']
for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Heat Generation'] = exp['Power']/(pi*d_i*pipe_length)

# Calculate the heat loss
k = 0.04154 # Insulation conduction coefficient (W/mK)
R = d_i*ln(d_0/d_i)/(2*pi*k) # Insulation thermal resistance (K/W)

measured_data['Heat Loss'] = None

index = 0
for test, data in tests.items():
	in_avg = float((data['TC8'].iloc[0] + data['TC10'].iloc[0] + data['TC12'].iloc[0]) / 3)	# Avg inside insulation temp
	out_avg = float((data['TC9'].iloc[0] + data['TC11'].iloc[0] + data['TC13'].iloc[0]) / 3) # Avg outside insulation temp
	measured_data.loc[index, 'Heat Loss'] = (in_avg - out_avg) / R # Heat loss through insulation
	index += 1

# Calculate the heat transfer
measured_data['Heat Transfer (q_gen - q_loss)'] = None

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Heat Transfer (q_gen - q_loss)'] = exp['Heat Generation'] - exp['Heat Loss']

# Splits the thermocouple readings by group
positions = tests['Test 1 - High MFR Low Crnt'].iloc[1].tolist()
inside_pipe_x = positions[:7] # 7 thermocouples inside pipe
outside_pipe_x = positions[7:13:2] # 3 thermocouples outside pipe and outside insulation (same position values)
tests_temps = {key:{'Outside Pipe':[], 'Inside Pipe':[], 'Outside Insulation':[]} for key in tests.keys()} # For recording temperature groups

# Splits the temperature data by group
for test, data in tests.items():
	temperatures = data.iloc[0].tolist()
	inside_pipe_temp = temperatures[:7]	# 7 thermocouples inside pipe
	outside_pipe_temp = temperatures[7:13:2] # 3 thermocouples outside pipe
	outside_insulation_temp = temperatures[8:14:2] # 3 thermocouples outside insulation
	tests_temps[test]['Inside Pipe'] = inside_pipe_temp
	tests_temps[test]['Outside Pipe'] = outside_pipe_temp
	tests_temps[test]['Outside Insulation'] = outside_insulation_temp

# Function to plot temperature groups readings vs position

def plot_groups(x, y_data, title, xlabel, ylabel, y_limits=None):
	sns.set_theme(style='darkgrid')
	fig, ax = plt.subplots()
	fig.canvas.manager.window.wm_geometry("+%d+%d" % (fig.canvas.manager.window.winfo_screenwidth() // 2 - fig.get_figwidth() * fig.dpi // 2, 
													  fig.canvas.manager.window.winfo_screenheight() // 2 - fig.get_figheight() * fig.dpi // 2))
	for label, y in y_data.items():
		ax.plot(x, y, label=label, marker='o', markersize=3)  # Add marker='o' to plot points along the line graph with smaller marker size
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	if y_limits:
		plt.ylim(y_limits)
	plt.legend()

# Function to plot temperature data for a single test
def plot_temps(test_name, test_data, title, xlabel, ylabel, y_limits=None):
	sns.set_theme(style='darkgrid')
	fig, ax = plt.subplots()
	fig.canvas.manager.window.wm_geometry("+%d+%d" % (fig.canvas.manager.window.winfo_screenwidth() // 2 - fig.get_figwidth() * fig.dpi // 2, 
													  fig.canvas.manager.window.winfo_screenheight() // 2 - fig.get_figheight() * fig.dpi // 2))
	ax.plot(inside_pipe_x, test_data['Inside Pipe'], label='Inside Pipe', marker='o', markersize=3, color='purple')
	ax.plot(outside_pipe_x, test_data['Outside Pipe'], label='Outside Pipe', marker='o', markersize=3, color='green')
	ax.plot(outside_pipe_x, test_data['Outside Insulation'], label='Outside Insulation', marker='o', markersize=3, color='darkblue')
	plt.title(f"{title} - {test_name}")
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	if y_limits:
		plt.ylim(y_limits)
	plt.legend()

# Plot the temperature groups
temperature_groups = {
	'Temperature Inside Pipe': ('Inside Pipe', inside_pipe_x),
	'Temperature Outside Pipe': ('Outside Pipe', outside_pipe_x),
	'Temperature Outside Insulation': ('Outside Insulation', outside_pipe_x)}

for title, (group, x) in temperature_groups.items():
	plot_groups(x, {test: data[group] for test, data in tests_temps.items()},
				title, 'Position (m)', 'Temperature (°C)', y_limits=(20, 100))

# Plot temperatures for each test
for test_name, test_data in tests_temps.items():
	plot_temps(test_name, test_data, 'Temperature Profile', 'Position (m)', 'Temperature (°C)', y_limits=(20, 100))

# Displays the plots
# plt.show()

# Calculate the mean bulk temperature
measured_data['Bulk Mean Temperature Slope'] = None

for [test, data], run in zip(tests_temps.items(), range(4)):
	measured_data.loc[run,'Bulk Mean Temperature Slope'] = (data['Inside Pipe'][4] - data['Inside Pipe'][2]) / (inside_pipe_x[4]-inside_pipe_x[2])

# Recalculate the heat transfer
c_p = 1009 # Specific heat capacity of air (J/kg*K)
measured_data['Heat Transfer (BMT)'] = None

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Heat Transfer (BMT)'] = c_p*exp['Mass Flow Rate']*(exp['Bulk Mean Temperature Slope']/(pi*d_i))

# Compute air temperature for each x value
predicted_temps = {}
for index, exp in measured_data.iterrows():
	bmt_slope = exp['Bulk Mean Temperature Slope']
	initial_temp = exp['Inlet Temp']
	predicted_temps[exp['Experiment']] = [(initial_temp + (position * bmt_slope))-273.15 for position in inside_pipe_x]

# Plot the predicted temperatures
for test_name, temps in predicted_temps.items():
	sns.set_theme(style='darkgrid')
	fig, ax = plt.subplots()
	fig.canvas.manager.window.wm_geometry("+%d+%d" % (fig.canvas.manager.window.winfo_screenwidth() // 2 - fig.get_figwidth() * fig.dpi // 2, 
													  fig.canvas.manager.window.winfo_screenheight() // 2 - fig.get_figheight() * fig.dpi // 2))
	ax.plot(inside_pipe_x, temps, label='Predicted Air Temp', marker='o', markersize=3, color='purple')
	ax.plot(inside_pipe_x, tests_temps[test_name]['Inside Pipe'], label='Measured Pipe Temp', marker='o', markersize=3, color='green')
	plt.xlabel('Position (m)')
	plt.title(f"{test_name} Predicted Temperatures")
	plt.ylabel('Temperature (°C)')
	plt.legend()

# PLot the difference between the predicted and measured temperatures
sns.set_theme(style='darkgrid')
fig, ax = plt.subplots()
fig.canvas.manager.window.wm_geometry("+%d+%d" % (fig.canvas.manager.window.winfo_screenwidth() // 2 - fig.get_figwidth() * fig.dpi // 2, 
												  fig.canvas.manager.window.winfo_screenheight() // 2 - fig.get_figheight() * fig.dpi // 2))

for test_name, temps in predicted_temps.items():
	temp_diff = [temps[i] - tests_temps[test_name]['Inside Pipe'][i] for i in range(7)]
	ax.plot(inside_pipe_x, temp_diff, label=f'{test_name} Wall vs Bulk', marker='o', markersize=3)

plt.xlabel('Position (m)')
plt.title('Wall vs Bulk Temperature Differences')
plt.ylabel('Temperature Difference (°C)')
plt.legend()

# Calculate heat transfer coefficient
measured_data['Heat Transfer Coefficient'] = None

for index, exp in measured_data.iterrows():
	pipe_temp = tests_temps[exp['Experiment']]['Inside Pipe'][3]
	air_temp = predicted_temps[exp['Experiment']][3]
	measured_data.loc[index, 'Heat Transfer Coefficient'] = exp['Heat Transfer (q_gen - q_loss)'] / (pipe_temp - air_temp)

# Theoretical Reynolds number
measured_data['Reynolds Number'] = None
air_viscosity = 1.846e-5 # Dynamic viscosity of air (kg/m*s)

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Reynolds Number'] = (4*exp['Mass Flow Rate'])/(air_viscosity*pi*d_i)

# Theoretical Nusselt number
measured_data['Theoretical Nu'] = None
prandtl_number = 0.707 # Prandtl number for air
k_air = 0.028 # Thermal conductivity of air (W/mK)

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Theoretical Nu'] = (exp['Heat Transfer Coefficient']*d_i)/k_air

# Correlated Nusselt number
measured_data['Correlated Nu'] = None

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Correlated Nu'] = 0.023*(exp['Reynolds Number']**0.8)*(prandtl_number**0.4)

# Theoretical friction factor
measured_data['Theoretical Friction Factor'] = None

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Theoretical Friction Factor'] = (2*(exp['Orifice Mano']-exp['Pipe Mano'])*water_density*9.81
	*exp['Air Density']*d_i*area_pipe**2/(exp['Mass Flow Rate']**2*pipe_length))

# Correlated friction factor
measured_data['Correlated Friction Factor'] = None

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Correlated Friction Factor'] = 0.316/(exp['Reynolds Number']**0.25)

# Theoretical stanton number
measured_data['Theoretical Stanton Number'] = None

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Theoretical Stanton Number'] = ((pi*d_i**2*exp['Heat Transfer Coefficient'])
															/(exp['Air Density']*c_p*exp['Mass Flow Rate']))

# Correlated stanton number
measured_data['Correlated Stanton Number'] = None

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Correlated Stanton Number'] = exp['Correlated Friction Factor']*prandtl_number**(-2/3)/8

# Writes the data to an excel file
output_path = os.path.join(current_dir, 'Forced Convection Calculations.xlsx')

# Check if the file exists, if not create it
if not os.path.exists(output_path):
	print()
	print(f'Creating file "Forced Convection Calculations.xlsx" at {output_path}')
	print()
	with open(output_path, 'w') as f:
		pass

with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
	measured_data.to_excel(writer, sheet_name='Calculations', index=False)
	workbook = writer.book
	worksheet = writer.sheets['Calculations']
	for column in measured_data:
		column_width = max(measured_data[column].astype(str).map(len).max(), len(column))
		col_idx = measured_data.columns.get_loc(column)
		worksheet.set_column(col_idx, col_idx, column_width)

os.startfile(output_path)
plt.show()
