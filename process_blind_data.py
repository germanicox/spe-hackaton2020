
import pandas as pd
pd.options.mode.chained_assignment = None  # avoid default='warn'
import sqlite3 as sql
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


conn = sql.connect('anh_production_data.db')

# all data base is loaded in memory pandas data frame
# all data mining and process is done in memory with pandas ;) 

production_df = pd.read_sql('SELECT * FROM anh_production_data', conn)

# for BONUS plotting every task requested plot init 


#now is time to go over every single requirement as stated here as follow: 
# Realice un análisis descriptivo de la producción que le permita responder las siguientes preguntas:

# Datos de Blind Test:

# 1 Caudal de producción del campo "1F D2689F", Julio 2019 - 2 puntos
# 2 Barriles producidos por la operadora "2FE52430" en Febrero 2019 - 2 puntos
# 3 Indique la producción departamental en barriles en el año 2018 - 2 puntos
# 4 Cuáles son los departamentos con producción promedio por campo mas variable - 2 puntos
# 5 Cuál es la tasa de declinación promedio mensual (Arps, hiperbólica, b = 0.5) del campo "51CBB05D" - 2 puntos

MONTHS = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']

# 1 Caudal de producción del campo "1F D2689F", Julio 2019 - 2 puntos
encrypted_field = 'AKACIAS'

#extract 2019 year / group by Campo and sum total production reported in Julio 
answer1 = production_df[production_df['YEAR']=='2019'][['CAMPO','JULIO']].groupby(['CAMPO'])['JULIO'].agg('sum')
print('*** Caudal de producción del campo "1F D2689F", Julio 2019 ***')
print(answer1[encrypted_field])

# fig = plt.figure()
# ax = fig.add_subplot(111)
# answer1.plot.pie()

del answer1

# 2 Barriles producidos por la operadora "2FE52430" en Febrero 2019 - 2 puntos
encrypted_operator =  'LEWIS ENERGY COLOMBIA INC'

#extract 2019 year / group by Operadora and sum total production reported in Febrero 
answer2 = production_df[production_df['YEAR']=='2019'][['OPERADORA', 'FEBRERO']].groupby(['OPERADORA'])['FEBRERO'].agg('sum')
print('\n*** Barriles producidos por la operadora "2FE52430", Julio 2019 ***')
print(answer2[encrypted_operator])

del answer2

# 3 Indique la producción departamental en barriles en el año 2018 - 2 puntos

#extract 2018 year / group by Departamento and sum each month total
answer3 = production_df[production_df['YEAR']=='2018'].groupby('DEPARTAMENTO')[MONTHS].agg('sum')
# add total year column 
answer3['TOTAL_PROD_YEAR'] = answer3.sum(axis=1)
print('\n*** Produccion Departamental en barriles, 2018 ***')
print(answer3.sort_values(by='TOTAL_PROD_YEAR', ascending=False) )

fig = plt.figure()
ax = fig.add_subplot(111)
answer3.plot(kind = 'bar')

plt.xlabel('Departamento')
plt.ylabel('Production BPDC')
plt.title("Comparacion de Produccion Departamental - 2018 \n (Use Zoom sobre la imagen para detalles de cada mes si se requiere)")

del answer3

# 4 Cuáles son los departamentos con producción promedio por campo mas variable - 2 puntos

# Group by Campo then by Year and sum production if more than one field is present 
answer4 = production_df.groupby(['DEPARTAMENTO','CAMPO','YEAR'])[MONTHS].agg('sum')

# Since calculations performed over mean, std deviation, etc 0 where no production is reported needs to be treated as NaN to fit Statistics rules 
answer4 = answer4.replace(0, np.NaN)
answer4["MEAN_PROD_YEAR"] = answer4.loc[:,MONTHS].mean(axis=1) 
answer4["STDdev_PROD_YEAR"] = answer4.loc[:,MONTHS].std(axis=1) 
answer4["VAR_PROD_YEAR"] = answer4.loc[:,MONTHS].var(axis=1)

answer4 = answer4.replace(np.NaN, 0)
print('\n*** Variabilidad promedios anuales por campo ***')
print(answer4.sort_values(by="STDdev_PROD_YEAR", ascending=False))

del answer4

# 5 Cuál es la tasa de declinación promedio mensual (Arps, hiperbólica, b = 0.5) del campo "51CBB05D" - 2 puntos

encrypted_field2 = 'QUIFA'

# Ecuacion que presenta Arps para el gasto de la declinacion hiperbolica es: 
#     q(t) =      q_i 
#           ---------------
#           (b*t*D_i +1) ^1/b

# q: Producción (bpd, pcd).
# q_i: Producción inicial (bpd, pcd)
# D: Rapidez de declinación (días-1)
# t:Tiempo (días)
# b: Exponente de declinación

#(Arps, hiperbólica, b = 0.5)
def hyperbolic_equation(t, qi, di):
    """
    Hyperbolic decline curve equation
    Arguments:
        t: Float. Time since the well first came online, can be in various units 
        (days, months, etc) so long as they are consistent.
        qi: Float. Initial production rate when well first came online.
        b: Float. Hyperbolic decline constant
        di: Float. Nominal decline rate at time t=0
    Output: 
        Returns q, or the expected production rate at time t. Float.
    """
    b=0.5
    return qi/((1.0+b*di*t)**(1.0/b))


# extract production data for requested Field 
answer5 = production_df[production_df['CAMPO'] == encrypted_field2].groupby(['CAMPO','YEAR'])[MONTHS].agg('sum')
answer5 = answer5.replace(0, np.NaN)
print('\n*** Tasa de declinación promedio mensual (Arps, hiperbólica, b = 0.5) del campo "51CBB05D" ***')
print(answer5)

# data in an array for curve_fit procesing 
production = np.array([])
production = np.append(production, answer5.iloc[0:3].values)
production = production[~np.isnan(production)]
time_months = np.arange(len(production)) 

# popt_hyp, pcov_hyp=curve_fit(hyperbolic_equation,


labels = answer5.columns

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(time_months,production, color='darkgreen', marker='^')
plt.yscale("log")


#Hyperbolic curve fit the data to get best fit equation
popt_hyp, pcov_hyp = curve_fit(hyperbolic_equation, production, time_months, bounds=(0, [production[0],45]))

hyp_approx = hyperbolic_equation(time_months, *popt_hyp)
print("Ajuste declinacion por metodo hiperbolico con b=0.5 = [q_1 , D]", popt_hyp)
# print(hyp_approx)

print("Tasa de declinacion con aprox Hyperbolica con b=0.5 es: ", popt_hyp[1])
ax.plot(time_months, hyp_approx)
plt.xlabel('Meses')
plt.ylabel('Production BPDC')
plt.title("Aproximacion Hyperbolica de Declinacion de Produccion con b=0.5")

del answer5
del production_df
plt.show()