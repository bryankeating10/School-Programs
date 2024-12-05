# LIBRARIES
from math import pow
from matplotlib import pyplot as plt

# CONSTANTS
h_e = [round(x * 1e-6,6) for x in range(1, 21)]
e_i = 1.93e11
v_i = 0.31
e_s_copper = 1.1e11
v_s_copper = 0.34
e_s_polyethylene = 1.1e9
v_s_polyethylene = 0.42
radius = 8e-9

# DATA


# FUNCTIONS
def composite_modulus(e_s,v_s):
	a = (1-pow(v_s,2))/e_s
	b = (1-pow(v_i,2))/e_i
	return 1/(a+b)


def force_calculator(r,h,e_star):
	a = pow(r,-1/3)
	b = pow(9/16,1/3)
	c = pow(h,3/2)*e_star
	return c/(a*b)


# CALCULATE THEORETICAL RESULTS
e_comp_copper = composite_modulus(e_s_copper,v_s_copper)
e_comp_polyethylene = composite_modulus(e_s_polyethylene,v_s_polyethylene)

print(f'E Comp Polyethylene: {e_comp_polyethylene}')
print(f'E Comp Copper: {e_comp_copper}')

force_copper = []
for i in range(20):
	force_copper.append(force_calculator(radius,h_e[i],e_comp_copper))

force_polyethylene = []
for i in range(20):
	force_polyethylene.append(force_calculator(radius,h_e[i],e_comp_polyethylene))

# DISPLAY THEORETICAL RESULTS
print("")
print("Forces for Copper")
for i in range(len(force_copper)):
	print(f'{force_copper[i]}')

print("")
print("Forces for Polyethylene")
for i in range(len(force_polyethylene)):
	print(f'{force_polyethylene[i]}')

# print("")
# print("Forces for Copper")
# for i in range(len(force_copper)):
# 	print(f'{h_e[i]}m: {force_copper[i]} N')

# print("")
# print("Forces for Polyethylene")
# for i in range(len(force_polyethylene)):
# 	print(f'{h_e[i]}m: {force_polyethylene[i]} N')

# PLOT



