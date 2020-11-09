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

from flask import Flask, render_template, request, jsonify, url_for
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

conn = sql.connect('datos_oficiales.db')
production_df = pd.read_sql('SELECT * FROM datos_oficiales', conn)
pd.options.display.float_format = '{:.2f}'.format
production_df = production_df.round(2)

COLUMNS = ['YEAR', 'DEPARTAMENTO', 'MUNICIPIO', 'OPERADORA', 'CONTRATO', 'CAMPO', 'YEAR']
MONTHS = ['ENERO', 'FEBRERO', 'MARZO', 'ABRIL', 'MAYO', 'JUNIO', 'JULIO', 'AGOSTO', 'SEPTIEMBRE', 'OCTUBRE', 'NOVIEMBRE', 'DICIEMBRE']

# column YEAR is moved to first position for simplicity in data show 
column_year = production_df.pop('YEAR')
production_df.insert(1, 'YEAR', column_year)

@app.route('/')
def index():
     datos = production_df.to_json(orient="table")
     return render_template('index.html', column_names=production_df.columns.values, 
                             row_data=list(production_df.values.tolist()),zip=zip,
                             unique_year = production_df['YEAR'].unique(),
                             unique_departamento = production_df['DEPARTAMENTO'].unique(),
                             unique_municipio = production_df['MUNICIPIO'].unique(),
                             unique_operadora = production_df['OPERADORA'].unique(),
                             unique_contrato = production_df['CONTRATO'].unique(),
                             unique_campo = production_df['CAMPO'].unique(),
                             

                             )


@app.route('/production_query', methods=['POST'])
def production_query():
    print("Call to production query: ...")

    app_data = request.form

    if not app_data['year_input'] == 'ALL' :
        requested_df = production_df[ production_df['YEAR'] == app_data['year_input'] ]
    else :
        requested_df = production_df

    if not app_data['departamento_input'] == 'ALL' :
        requested_df = requested_df[production_df['DEPARTAMENTO'] == app_data['departamento_input'] ]

    if not app_data['municipio_input'] == 'ALL' :
        requested_df = requested_df[production_df['MUNICIPIO'] == app_data['municipio_input'] ]

    if not app_data['operadora_input'] == 'ALL' :
        requested_df = requested_df[production_df['OPERADORA'] == app_data['operadora_input'] ]

    if not app_data['contrato_input'] == 'ALL' :
        requested_df = requested_df[production_df['CONTRATO'] == app_data['contrato_input'] ]

    if not app_data['campo_input'] == 'ALL' :
        requested_df = requested_df[production_df['CAMPO'] == app_data['campo_input'] ]

    requested_df = requested_df.reset_index()

    print(requested_df)  
  
    if not requested_df.empty :
        total_production = requested_df[MONTHS].agg('sum')
        fig = plt.figure() 
        total_production.plot(kind='bar', title = 'Produccion Total Mensual')
        plt.ylabel("BPD")
        plt.tight_layout()
        # plt.show()
        plt.savefig('./static/grafico.png')
        plt.close()
        print(total_production)
        return  ( requested_df.to_json() ) 


        #if empty data frame is returned is because Query is not OK
    else :
        print("Error Not data found ...")
        return  ( {
                    'error' : "ERROR" } ) 

if __name__ == '__main__':
    app.run(debug=True)
    # print(production_df)
    print(production_df['YEAR'].unique())

