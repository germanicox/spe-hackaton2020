
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sqlite3 as sql
import matplotlib.pyplot as plt


print("This script is designed to cover 5 request fro Descriptive Analisys for SPE-COL-Hackaton (DATOS OFICIALES)")
print("IS EXPECTED TO RUN PREVIOUSLY <<read_and_process.py>> script to read / format data and store in SQLlite database ...")

# filename = sys.argv[count_input_file+1]


conn = sql.connect('prueba_de_fuego.db')

# all data base is loaded in memory pandas data frame
# all data mining and process is done in memory with pandas ;) 

production_df = pd.read_sql('SELECT * FROM prueba_de_fuego', conn)

# for BONUS plotting every task requested plot init 


#now is time to go over every single requirement as stated here as follow: 
# Realice un análisis descriptivo de la producción que le permita responder las siguientes preguntas:

# Datos Oficiales:

# 1 - Indique el top 5 de los campos con mayor producción durante el año 2020 - 2 puntos
# 2 - Indique cuántas y cuáles compañias han reportado producción en más de 5 campos en Casanare en el año 2018 - 2 puntos
# 3 - Indique los 5 contratos con la más alta producción en MMstb en el año 2018 - 2 puntos
# 4 - Ordene de mayor a menor las 10 Operadoras con mayor produccion en el mes de agosto 2019 - 2 puntos
# 5 - Realice un análisisis comparativo de la producción de los dos primeros trimestres de los años 2019 y 2020. Trimestres: Enero a Marzo, Abril a Junio - 2 puntos

MONTHS = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']

# 1 - Indique el top 5 de los campos con mayor producción durante el año 2020 - 2 puntos
answer1 = production_df[production_df['YEAR']=='2020']
answer1['TOTAL_PROD_YEAR'] = production_df.loc[:, MONTHS].sum(axis=1)
answer1 = (answer1.groupby(['CAMPO'])['TOTAL_PROD_YEAR'].agg('sum')).sort_values(ascending=False).head(5)
# if you want include more data in order, lets say top 10 just replace ...head(10) in the line above 
print('*** Top 5 - Campos con Mayor Produccion (2020) ***')
print(answer1)
# ****** BONUS PLOT 
# ax_1 = fig.add_subplot(321)
fig = plt.figure()
fig.tight_layout()
answer1.plot(kind='barh', title = 'Top 5 - Campos con Mayor Produccion (2020)')
plt.xlabel('Produccion - BPDC')
plt.gca().invert_yaxis()

del answer1

# 2 - Indique cuántas y cuáles compañias han reportado producción en más de 5 campos en Casanare en el año 2018 - 2 puntos
answer2 = production_df[production_df['YEAR']=='2018']
answer2 = answer2[answer2['DEPARTAMENTO']=='CASANARE']
# DataFrame.nunique() Count distinct observations over requested axis  *** because some field are more than once in Casanare for same Operator
answer2 = answer2.groupby(['OPERADORA'])['CAMPO'].nunique().sort_values(ascending=False)
print('\n*** Las siguientes companias han reportado produccion en mas de 5 campos en Casanare (2018) ***')
print("Cuantas Operadoras han reportado produccion en mas de 5 Campos? ", answer2[answer2 > 5].count())
print("Cuales son? ")
print(answer2[answer2 > 5])
# ****** BONUS PLOT 
fig = plt.figure()
# ax_2 = fig.add_subplot(322)
fig.tight_layout()
answer2[answer2>5].plot(kind='barh', title = 'Operadoras con produccion en mas de 5 Campos en Casanare (2018)')
plt.xlabel('# Campos de Operacion por Operadora')
plt.gca().invert_yaxis()
del answer2

# 3 - Indique los 5 contratos con la más alta producción en MMstb en el año 2018 - 2 puntos
answer3 = production_df[production_df['YEAR']=='2018']
answer3['TOTAL_PROD_YEAR'] = production_df.loc[:, MONTHS].sum(axis=1)
answer3 = (answer3.groupby(['CONTRATO'])['TOTAL_PROD_YEAR'].agg('sum')).sort_values(ascending=False).head(5)
print('\n*** Top 5 - Contratos con Mayor Produccion (2018) ***')
print(answer3)
# ****** BONUS PLOT 
fig = plt.figure()
# ax_3 = fig.add_subplot(323)
fig.tight_layout()
answer3.plot(kind='barh', title='Top 5 - Contratos con Mayor Produccion (2018)')
plt.xlabel('Produccion - BPDC')
plt.gca().invert_yaxis()
del answer3

# 4 - Ordene de mayor a menor las 10 Operadoras con mayor produccion en el mes de agosto 2019 - 2 puntos
answer4 = production_df[production_df['YEAR']=='2019']
answer4 = answer4.groupby(['OPERADORA'])['AGOSTO'].agg('sum').sort_values(ascending=False).head(10)
print('\n*** Top 10 - Operadoras con Mayor Produccion en el mes de Agosto 2019 ***')
print(answer4)
# ****** BONUS PLOT 
fig = plt.figure()
# ax_4 = fig.add_subplot(324)
fig.tight_layout()
answer4.plot(kind='barh', title='Top 10 - Operadoras con Mayor Produccion en el mes de Agosto 2019')
plt.xlabel('Produccion - BPDC')
plt.gca().invert_yaxis()
# ax_4.set(xlabel='Produccion - BPDC')
del answer4

# 5 - Realice un análisisis comparativo de la producción de los dos primeros trimestres de los años 2019 y 2020. Trimestres: Enero a Marzo, Abril a Junio - 2 puntos
Q1 = ['ENERO', 'FEBRERO', 'MARZO']
Q2 = ['ABRIL', 'MAYO', 'JUNIO']

answer5_Q1_2019 = production_df[ (production_df['YEAR'] == '2019') ][Q1].sum()
answer5_Q1_2019['Q1'] = answer5_Q1_2019[Q1].sum()
answer5_Q1_2019 = answer5_Q1_2019.to_frame()
answer5_Q1_2019.columns = ['2019']

answer5_Q1_2020 = production_df[ (production_df['YEAR'] == '2020') ][Q1].sum()
answer5_Q1_2020['Q1'] = answer5_Q1_2020[Q1].sum()
answer5_Q1_2020 = answer5_Q1_2020.to_frame()
answer5_Q1_2020.columns = ['2020']

#2019 vs 2020 comparision focus on production evolution and % of this evolution in both years
# Production 2020 - Production 2019 
# % as (Production 2020 - Production 2019) / Production 2019

answer5_Q1 = answer5_Q1_2019.merge(answer5_Q1_2020, left_index=True, right_index=True)
answer5_Q1['COMPARE'] = answer5_Q1['2020'] - answer5_Q1['2019']
answer5_Q1['%'] = round((answer5_Q1['COMPARE'] / answer5_Q1['2019'])*100 , 1)

answer5_Q2_2019 = production_df[ (production_df['YEAR'] == '2019') ][Q2].sum()
answer5_Q2_2019['Q2'] = answer5_Q2_2019[Q2].sum()
answer5_Q2_2019 = answer5_Q2_2019.to_frame()
answer5_Q2_2019.columns = ['2019']


answer5_Q2_2020 = production_df[ (production_df['YEAR'] == '2020') ][Q2].sum()
answer5_Q2_2020['Q2'] = answer5_Q2_2020[Q2].sum()
answer5_Q2_2020 = answer5_Q2_2020.to_frame()
answer5_Q2_2020.columns = ['2020']

#2019 vs 2020 comparision focus on production evolution and % of this evolution in both years
# Production 2020 - Production 2019 
# % as (Production 2020 - Production 2019) / Production 2019

answer5_Q2 = answer5_Q2_2019.merge(answer5_Q2_2020, left_index=True, right_index=True)
answer5_Q2['COMPARE'] = round(answer5_Q2['2020'] - answer5_Q2['2019'], 2)
answer5_Q2['%'] = round((answer5_Q2['COMPARE'] / answer5_Q2['2019'])*100 , 1)

print('\n*** Analisis comparativo Produccion Q1 2019/2020 ***')
print(answer5_Q1)
print(answer5_Q2)

# ****** BONUS PLOT 
y_min = min(answer5_Q1[['2019', '2020']].min())*0.95 #scale Y-axis min limits for plot
y_max = max(answer5_Q1[['2019', '2020']].max())*1.05 #scale Y-axis min limits for plot


fig1 = plt.figure()
ax_5 = fig1.add_subplot(221)
answer5_Q1.loc[Q1, ['2019', '2020']].plot(kind='bar', title='Analisis comparativo Produccion Q1 2019/2020')
ax_5.set(ylim=[y_min, y_max])

plt.show()

