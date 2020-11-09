#______________________________________________________
# Author: German Barboza                               |
# email: germanbarboza@gmail.com                       |
# github: germanicox                                   |
# twitter: germanicox                                  |
# linkedin: https://www.linkedin.com/in/gbarboza2020/  |
#______________________________________________________

# November - 2020
# This script is inented to solve data collection and format for SPE-2020 Colombia Section Hackaton 
# Details at: https://github.com/specolombiahackathon/202010/wiki

import sqlite3 as sql
import pandas as pd
import numpy as np
import math

# all data base is loaded in memory pandas data frame
# all data mining and process is done in memory with pandas ;) 

COLUMNS_TO_GUESS = ['DEPARTAMENTO', 'MUNICIPIO', 'OPERADORA', 'CONTRATO', 'CAMPO', 'YEAR']
MONTHS = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']

conn = sql.connect('datos_oficiales.db')
datos_originales_df = pd.read_sql('SELECT * FROM datos_oficiales', conn)

conn = sql.connect('datos_blind_test.db')
datos_blind_df = pd.read_sql('SELECT * FROM datos_blind_test', conn)

#identify some inconsistencies on data spaces, - etc 
#remove and apply over entire Blind Data

original_data = datos_originales_df[COLUMNS_TO_GUESS]
blind_data = datos_blind_df[COLUMNS_TO_GUESS].applymap(lambda x: x.replace(" ", "").replace("-","") if isinstance(x, str) else x)
array_datos = np.array(datos_originales_df[MONTHS])
array_blind = np.array(datos_blind_df[MONTHS])
mean_square = 0

DEBUG = False
#THE FOLLOWING CODE identify arounnd *****************************************************************
#is to proper visualize unique values per column and data insights for Data Engineer Visualization 
# no automation process based on this insights 

if DEBUG : 
    how_many_unique_DEPARTAMENTO = blind_data['DEPARTAMENTO'].unique()

    how_many_unique_MUNICIPIO = blind_data['MUNICIPIO'].unique()
    how_many_unique_OPERADORA = blind_data['OPERADORA'].unique()
    how_many_unique_CONTRATO = blind_data['CONTRATO'].unique()
    how_many_unique_CAMPO = blind_data['CAMPO'].unique()

    print(how_many_unique_DEPARTAMENTO, len(how_many_unique_DEPARTAMENTO))
    print(how_many_unique_MUNICIPIO, len(how_many_unique_MUNICIPIO))
    print(how_many_unique_OPERADORA, len(how_many_unique_OPERADORA))
    print(how_many_unique_CONTRATO, len(how_many_unique_CONTRATO))
    print(how_many_unique_CAMPO, len(how_many_unique_CAMPO))


    unique_encrypted = pd.DataFrame([how_many_unique_DEPARTAMENTO , how_many_unique_MUNICIPIO, how_many_unique_OPERADORA, how_many_unique_CONTRATO, how_many_unique_CAMPO])
    # print("Unique values: ", unique_encrypted[:,:].unique())

# print(blind_data['DEPARTAMENTO','CAMPO'].unique())


#****************************************************************************************************************



pd.set_option("display.max_rows", None)
print("\nOriginal Encrypted Data ... ")
print(blind_data)

enigma_solution = {"dato": [], "encrypted": []}
# enigma_solution = {"cf33cb8a": "ARAUCA"}
# iterate over ALL rows in blind data table 

# for i in array_blind :
for i in blind_data.iterrows() :
    # print(i[1])
    mse = []
    # each array of production data compose of MONTHS (12 float columns values) is 
    # evaluated over entire DATA OFICIAL production rows to calculate MSE (Mean Square Error)
    # in this way we can capture adjustment level on both array (production data) since looks like
    # blind data production was close to data oficial but some random noise entered (my guess ; !!!!!) ) 
    for each in array_datos :
        # print(each)
        # mean_square = np.square(np.subtract(each, i)).mean()
        mean_square = np.square(np.subtract(each, array_blind[i[0]])).mean() 
        mse.append(mean_square)  # this variable is to compare out of this for to find out for min MSE
    #this index has best match based on MSE (Mean Square Error) and data from Datos Oficiales are being 
    #copy to replace blind data 
    #to register value par Datos - Oficial - Blind a dictionary is being created for register porpouse
    
    indice_min = mse.index(min(mse))
    # print("indice for mse(min): ", indice_min)

    # for every possible succesfull decoding ask if its 1st occurence to store in dictionary 
    # if is not in dict .... will be added as first and unique occurence 
    if not ( (i[1]['DEPARTAMENTO']) in enigma_solution['encrypted'] ) :
        enigma_solution["dato"].append(original_data.iloc[indice_min]['DEPARTAMENTO'])
        enigma_solution["encrypted"].append(i[1]['DEPARTAMENTO'])
    if not ( (i[1]['MUNICIPIO']) in enigma_solution['encrypted']) :
        enigma_solution["dato"].append(original_data.iloc[indice_min]['MUNICIPIO'])
        enigma_solution["encrypted"].append(i[1]['MUNICIPIO'])
    if not ( (i[1]['OPERADORA']) in enigma_solution['encrypted']) :
        enigma_solution["dato"].append(original_data.iloc[indice_min]['OPERADORA'])
        enigma_solution["encrypted"].append(i[1]['OPERADORA'])
    if not ( (i[1]['CONTRATO']) in enigma_solution['encrypted']) :
        enigma_solution["dato"].append(original_data.iloc[indice_min]['CONTRATO'])
        enigma_solution["encrypted"].append(i[1]['CONTRATO'])
    if not ( (i[1]['CAMPO']) in enigma_solution['encrypted']) :
        enigma_solution["dato"].append(original_data.iloc[indice_min]['CAMPO'])
        enigma_solution["encrypted"].append(i[1]['CAMPO'])
    


pd.set_option("display.max_rows", None)

solution = pd.DataFrame.from_dict(enigma_solution).sort_values(by='dato')

for row in solution.iterrows() :
    # print(row[1]['dato'])
    blind_data = blind_data.replace(row[1]['encrypted'], row[1]['dato'])

print("\nData recovery ... based on MSE (Mean Squared Error) error comparision to Original Data ... ")
print(blind_data)
print("\nSolution for Dictionary of keys values: ")
print(solution)

