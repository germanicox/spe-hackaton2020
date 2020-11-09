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

app = Flask(__name__)

conn = sql.connect('datos_oficiales.db')
production_df = pd.read_sql('SELECT * FROM datos_oficiales', conn)
pd.options.display.float_format = '{:.2f}'.format
production_df = production_df.round(2)
# production_df = production_df.set_index(keys='YEAR')

print(production_df.columns)

@app.route('/')
def index():
     datos = production_df.to_json(orient="table")
     return render_template('index.html', column_names=production_df.columns.values, row_data=list(production_df.values.tolist()),
                            zip=zip)



if __name__ == '__main__':
    app.run(debug=True)
    print(production_df)

