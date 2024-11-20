import pandas as pd
import matplotlib.pyplot as plt

# Constants
l = 0.02				# Length of metals
t = 50e-6				# Thickness of metals
alpha_n = 1.2e-5 		# Thermal expansion coeff of nickel
e_nickel = 2e11			# Young's modulus for nickel
t0 = 22					# Room temperature

# Accesses the simulation results from excel
file_path = "Bimetallic Ansys Results.xlsx"
df_tec = pd.read_excel(file_path,sheet_name="Thermal Expansion Coefficient")
df_ym = pd.read_excel(file_path,sheet_name="Young's Modulus")
df_temp = pd.read_excel(file_path,sheet_name="Temperature")

# Experimental values
delta_tec = df_tec['Experimental Deformation (m)'].tolist()
delta_ym = df_ym['Experimental Deformation (m)'].tolist()
delta_temp = df_temp['Experimental Deformation (m)'].tolist()

# Control values
control_tec = [2.3e-5]*11
control_ym = [7.1e10]*11
control_temp= [50]*11

# Parameterized values
para_tec = df_tec['Thermal Expansion Coefficient'].tolist()
para_ym = df_ym["Young's Modulus (Pa)"].tolist()
para_temp = df_temp['Temperature (C)'].tolist()

# Converts deformation to radius of curvature
def del_to_rad(deformation,length):
	radius = []
	for defo in deformation:
		radius.append(length**2/(2*defo))
	return radius

# Calculates theoretical radius of curvature
def theo_rad_curv(h,e1:list,e2,a1:list,a2,t:list,t0):
	radius = []
	for i in range(11):
		num = h*(14+(e1[i]/e2)+e2/e1[i])
		den = (a2-a1[i])*(t0-t[i])
		radius.append(num/den)
	return radius

# Experimental radius of curvatures
r_tec = del_to_rad(delta_tec,l)
r_ym = del_to_rad(delta_ym,l)
r_temp = del_to_rad(delta_temp,l)

# Theoretical radius of curvatures
theo_r_tec = theo_rad_curv(t,control_ym,e_nickel,para_tec,alpha_n,control_temp,t0)
theo_r_ym = theo_rad_curv(t,para_ym,e_nickel,control_tec,alpha_n,control_temp,t0)
theo_r_temp = theo_rad_curv(t,control_ym,e_nickel,control_tec,alpha_n,para_temp,t0)

# Thermal expansion coefficient results
print(f'Thermal Expansion Coeff (Exp): \n{r_tec}')
print(f'Thermal Expansion Coeff (Theo): \n{theo_r_tec}')
print("")

# Young's Modulus results
print(f"Young's Modulus (Exp): \n{r_ym}")
print(f"Young's Modulus (Theo): \n{theo_r_ym}")
print("")

# Temperature results
print(f'Temperature (Exp): \n{r_temp}')
print(f'Temperature (Theo): \n{theo_r_temp}')

plt.figure('TEC')
plt.plot(para_tec,r_tec,marker='.',markersize=10,label="Experimental")
plt.plot(para_tec,theo_r_tec,color='orange',marker='.',markersize=10,label="Theoretical")
plt.title('Radius of Curvature for Thermal Expansion Coeff')
plt.xlabel('Thermal Expansion Coefficient (m/m)')
plt.ylabel('Radius of Curvature (m)')
plt.legend()
plt.grid(True)
# plt.show()

plt.figure('YM')
plt.plot(para_ym,r_ym,marker='.',markersize=10,label="Experimental")
plt.plot(para_ym,theo_r_ym,color='orange',marker='.',markersize=10,label="Theoretical")
plt.title("Radius of Curvature for Young's Modulus")
plt.xlabel("Young's Modulus (Pa)")
plt.ylabel('Radius of Curvature (m)')
plt.legend()
plt.grid(True)
# plt.show()

plt.figure('T')
plt.plot(para_temp,r_temp,marker='.',markersize=10,label="Experimental")
plt.plot(para_temp,theo_r_temp,color='orange',marker='.',markersize=10,label="Theoretical")
plt.title('Radius of Curvature for Temperature')
plt.xlabel('Temperature (C)')
plt.ylabel('Radius of Curvature (m)')
plt.legend()
plt.grid(True)
plt.show()