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

import pandas as pd         # data structure in memory for data manipulation and load Excel data in python table
import xlrd as xlrd         # to manage and parse excel file to identify sheet structure, header, footage since noticed could be variable
import sqlite3 as sql
from sqlite3 import Error   # (Optional requirement) for SQLite requirement 
import sys                  #to manage files as input arguments for procesing 
import os.path              #to valid file passed as arguments if exist 
import urllib3              # to acces url and download files from ANH

production_df = pd.DataFrame()  #temporary dataframe for excel load 
df = pd.DataFrame() #to append and store full data set entered based on files input variable
#files detected as arguments 

def proccesing_excel__input_file(filename) :
    
    #boolean variable to identify possible no standard format from ANH as seen in Blind Test  
    format_is_ANH = True 
    
    book = xlrd.open_workbook(filename)
    print("The number of worksheets is {0}".format(book.nsheets))
    print("Worksheet name(s): {0}".format(book.sheet_names()))
    sh = book.sheet_by_index(0)
    print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))

    #iterate over rows in excel file looking for: 
    # (1) how long hader is and as consequence where data table starts 
    # (2) footage long: since noticed some files has total additional row and a comment about ANH its not uniform between files 
    # (3) year of the data table is get from header info instead of filename 
    find_footage = False
    year_found = False
    data_year = 0
    header_ends = 0
    footage = 0

    #footage could be present in two ways: as total row in which case is empty at start OR 
    #a comment seen as: Fuente: ANH / Sistema Oficial de Liquidación y Administración de Regalías - SOLAR
    rx = sh.nrows
    if (sh.cell_value(rowx=rx-1, colx=0)) == '' :
        footage = 1  #footage format in a row where TOTALS per column is present in oficial ANH format
    else :
        #two possible options: there is last data row ? or it's comment from ANH source format ?
        if sh.cell_value(rowx=rx-1, colx=1) =='' :
            footage = 2  # some ANH files include a message informative from ANH in its first column row
        else :
            #definetly it is NOT ANH file format - lets procees it as BLIND_TEST
             footage = 0  #no footage 
             header_ends = 0 #no header - first row is directly columns name 
            #  data_year = '2017' 
             print(filename)
             year = filename.find('20')
             data_year = filename[year:year+4]
             format_is_ANH = False 

    if format_is_ANH : 
        for rx in range(sh.nrows) :
            listToStr = ' '.join(str(elem) for elem in sh.row(rx))
            year = listToStr.find('20') #looking for year in header ONLY WORKS for years >= 2000
        
            if (year != -1) & (year_found==False):  
                #year TAG found in header
                data_year = listToStr[year:year+4]         
                year_found = True
        
            if (sh.cell_value(rowx=rx, colx=0) == 'Departamento' ) or (sh.cell_value(rowx=rx, colx=0) == 'concatenar' ) :
                header_ends = rx
                return data_year , header_ends , footage
    
    else :
        return data_year , header_ends , footage

    


def read_files_and_bring_data_to_pandas (files) :   
    global df
    global production_df

    for each in files : 
        print(each)
        print("procesing File input# ")
        print("Filename: " , each)
    
        data_year, header_ends, footage = proccesing_excel__input_file(each)

        df = pd.read_excel(each, header=header_ends, skipfooter=footage)
        df['year'] = data_year

        #all columns name in upper case letter ; since noticed some inconsistencies in files as Enero , enero 
        df = df.rename(str.upper, axis='columns')

        print(df.head())
        print(df.tail())
        print(df.shape)
        # print(df.info())
        production_df = production_df.append(df)

def create_connection(db_file) :
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sql.connect(db_file)
        print(sql.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def internet_on():
    try:
        urllib3.urlopen('http://www.anh.gov.co/', timeout=3)
        return True
    except urllib2.URLError as err: 
        return False

def go_to_ANH_and_download_files(*files) :

    http = urllib3.PoolManager()
 
    r = http.request('GET', files[0][1])
    print(r.status) 
    f = open(files[0][0], 'wb')
    f.write(r.data)
    f.close()

    r = http.request('GET', files[1][1])
    print(r.status)
    f = open(files[1][0], 'wb')
    f.write(r.data)
    f.close()

    r = http.request('GET', files[2][1])
    print(r.status)
    f = open(files[2][0], 'wb')
    f.write(r.data)
    f.close()


# ********************** 
# EXPECTED ARGUMENTS FOR count_input_file
# *********************************************
# > python read_and_process.py arg1 arg2 arg3 *
#**********************************************
how_many_input_files = len(sys.argv) - 1 
count_input_file = 0


#no input file - script ends with a message
if how_many_input_files == 0 :
    print("ERROR - YOU MUST ENTER AT LEAST ONE EXCEL VALID FILE FOR PROCESING")
    exit()

#user can select option to auto data files downloads from ANH 
#is expected an user input while executing this script as follow 
#***********************************
# >python read_and_process.py auto *
#***********************************

auto_files_from_web = False
filename2018 = ["archivo_descargado2018.xlsx" ,"http://www.anh.gov.co/Operaciones-Regal%C3%ADas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%C3%B3n%20Fiscalizada%20Crudo%202018.xlsx"]
filename2019 = ["archivo_descargado2019.xlsx" , "http://www.anh.gov.co/Operaciones-Regal%C3%ADas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%C3%B3n%20Fiscalizada%20Crudo%202019-DIC.xlsx"]
filename2020 = ["archivo_descargado2020.xlsx" , "http://www.anh.gov.co/Operaciones-Regal%C3%ADas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documentos%20compartidos/Producci%C3%B3n%20Fiscalizada%20Crudo%202020%20Agosto.xlsx"]
filename_from_web = [filename2018[0], filename2019[0], filename2020[0]]

# if auto is passed as argument -> Automation input from 
if ((sys.argv[-1] == 'auto') or  (sys.argv[-1] == 'web') or (sys.argv[-1] == 'WEB') or (sys.argv[-1] == 'AUTO') ) :
    auto_files_from_web = True
    
    print("You have selected auto web scrapping to ANH repository to download DATA for 2018, 2019 and 2020 excel files ...")

    go_to_ANH_and_download_files(filename2018, filename2019, filename2020)
    
    #now the files are locally stored as excel files in ./ 
    #accesing each file for processing
    read_files_and_bring_data_to_pandas(filename_from_web)

    
else :  #process every excel file that was passed as arguments 
    #iterate over arguments passed could be 1 file , 2 files or 3 files (expected for 2018, 2019 and 2020)
    filename_from_input = sys.argv[1:len(sys.argv)]
    read_files_and_bring_data_to_pandas(filename_from_input)   

production_df = production_df.fillna(0)

# BONUS 
#Lets manage database output 
# from pandas DataFrame to SQLite 

print("\n\nEnter a name for database SQL generation, hit enter to continue with assigned database name: anh_production_data.db (REPLACED DATABASE RISK) :" )
answer = input()

if answer == '':
    print("You have decided to procced with default name: anh_production_data.db, thanks and enjoy your Data Mining ...")
    # conn = sql.connect('anh_production_data.db')
    # production_df.to_sql('anh_production_data', conn, if_exists='replace')
    answer = 'anh_production_data'
else : 
    print("Succesfully database creation as:  <<", answer, ".db>> thanks and enjoy your Data Mining ...")

conn = sql.connect(answer+'.db')
production_df.to_sql(answer, conn, if_exists='replace')




