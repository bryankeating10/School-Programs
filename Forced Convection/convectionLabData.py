import pandas as pd
from math import sqrt, log as ln, pi

# Read in the temperature data 
file_path = r'Formatted Test Data.xlsx'
excel_file = pd.ExcelFile(file_path)
tests = {'Test 1 - High MFR Low Crnt': None, 'Test 2 - High MFR High Crnt': None, 
         'Test 3 - Low MFR High Crnt': None, 'Test 4 - Low MFR Low Crnt': None}

for sheet_name, test in zip(excel_file.sheet_names, tests):
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    tests[test] = df

# Read in the measured data
file_path = r'Measured Data.xlsx'
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
measured_data['Heat Transfer'] = None

for index, exp in measured_data.iterrows():
	measured_data.loc[index, 'Heat Transfer'] = exp['Heat Generation'] - exp['Heat Loss']
print(measured_data)