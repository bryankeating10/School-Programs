# Each description precedes its corresponding function.
'''
Description:
Converts Watts to Horsepower.

Parameters:
Watts (float): Power in Watts.

Output:
Horsepower (float): Power in Horsepower.
'''
def mbp_conversion(watts):
	return watts / 745.7

'''
Description:
Converts m^3/s to gallons per minute (GPM).

Parameters:
m3s (float): Flow rate in cubic meters per second.

Output:
Gallons per minute (float): Flow rate in gallons per minute.
'''

def ffr_conversion(m3s):
	return m3s * 15850.3

'''
Description:
Converts kg/Nm to lb/hp-hr.

Parameters:
kgperNm (float): Brake specific fuel consumption in kg/Nm.

Output:
lbperhpHr (float): Brake specific fuel consumption in lb/hp-hr.
'''
def bsfc_conversion(kgperNm):
	return kgperNm * 0.0005 * 3600 / 2.20462

'''
Description:
Converts Pa to psi.

Parameters:
Pa (float): Pressure in Pascals.

Output:
psi (float): Pressure in psi.
'''
def bmep_conversion(Pa):
	return Pa / 6894.76

'''
Convert Nm to lb-ft.

Parameters:
Nm (float): Torque in Newton-meters.

Output:
lbft (float): Torque in pound-feet.
'''
def torque_conversion(Nm):
	return Nm * 0.737562



