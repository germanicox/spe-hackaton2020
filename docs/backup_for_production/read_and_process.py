
import pandas as pd         # data structure in memory for data manipulation and load Excel data in python table
import xlrd as xlrd         # to manage and parse excel file to identify sheet structure, header, footage since noticed could be variable
import sqlite3 as sql
from sqlite3 import Error   # (Optional requirement) for SQLite requirement 
import sys                  #to manage files as input arguments for procesing 
import os.path              #to valid file passed as arguments if exist 
import urllib3




def create_connection(db_file):
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

def proccesing_excel__input_file(filename) :
    
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
        footage = 1
    else :
        footage = 2

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
             
# print (sys.argv)
# print (len(sys.argv))


#evaluating arguments from input command lines 

# ********************** 
# EXPECTED ARGUMENTS FOR count_input_file
# **********************

# > python read_and_process.py arg1 arg2 arg3  
how_many_input_files = len(sys.argv) - 1 
count_input_file = 0


"/Operaciones-Regalías-y-Participaciones/Sistema-Integrado-de-Operaciones/Documentos%20compartidos/Producción%20Fiscalizada%20Crudo%202020%20Agosto.xlsx"

auto_files_from_web = False
filename2018 = ["archivo_descargado2018.xlsx" ,"http://www.anh.gov.co/Operaciones-Regal%C3%ADas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%C3%B3n%20Fiscalizada%20Crudo%202018.xlsx"]
filename2019 = ["archivo_descargado2019.xlsx" , "http://www.anh.gov.co/Operaciones-Regal%C3%ADas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documents/Producci%C3%B3n%20Fiscalizada%20Crudo%202019-DIC.xlsx"]
filename2020 = ["archivo_descargado2020.xlsx" , "http://www.anh.gov.co/Operaciones-Regal%C3%ADas-y-Participaciones/Sistema-Integrado-de-Operaciones/Documentos%20compartidos/Producci%C3%B3n%20Fiscalizada%20Crudo%202020%20Agosto.xlsx"]
filename_from_web = [filename2018[0], filename2019[0], filename2020[0]]
#no input file - script ends with a message
if how_many_input_files == 0 :
    print("ERROR - YOU MUST ENTER AT LEAST ONE EXCEL VALID FILE FOR PROCESING")
    exit()

df = pd.DataFrame() #temporary dataframe for excel load 
production_df = pd.DataFrame() #to append and store full data set entered based on files input variable
#files detected as arguments 



#user can select option to auto data files downloads from ANH 
if ((sys.argv[-1] == 'auto') or  (sys.argv[-1] == 'web') or (sys.argv[-1] == 'WEB') or (sys.argv[-1] == 'AUTO') ) :
    auto_files_from_web = True
    
    print("You have selected auto web scrapping to ANH repository to download DATA for 2018, 2019 and 2020 excel files ...")
    outfilename = "./downloaded_2018.xlsx"
    http = urllib3.PoolManager()
    
    r = http.request('GET', filename2018[1])
    print(r.status)
    f = open(filename2018[0], 'wb')
    f.write(r.data)
    f.close()

    r = http.request('GET', filename2019[1])
    print(r.status)
    f = open(filename2019[0], 'wb')
    f.write(r.data)
    f.close()

    r = http.request('GET', filename2020[1])
    print(r.status)
    f = open(filename2020[0], 'wb')
    f.write(r.data)
    f.close()

    for each in filename_from_web : 
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

   

else :  #process every excel file that was passed as arguments 
    #iterate over arguments passed could be 1 file , 2 files or 3 files (expected for 2018, 2019 and 2020)

    filename_from_input = sys.argv[1:len(sys.argv)]
    for each in filename_from_input :
        print(each)

    while count_input_file < how_many_input_files :

        print("procesing File input# ", count_input_file+1)
        print("Filename: " , sys.argv[count_input_file+1])
    
        filename = sys.argv[count_input_file+1]
        data_year, header_ends, footage = proccesing_excel__input_file(filename)

        df = pd.read_excel(filename, header=header_ends, skipfooter=footage)
        df['year'] = data_year

        #all columns name in upper case letter ; since noticed some inconsistencies in files as Enero , enero 
        df = df.rename(str.upper, axis='columns')

        print(df.head())
        print(df.tail())
        print(df.shape)
        # print(df.info())
    
        production_df = production_df.append(df)

        #END - while loop for file procesing 
        count_input_file += 1


production_df = production_df.fillna(0)
# print(production_df.shape)
# print(production_df)



print("\n\nEnter a name for database SQL generation, hit enter to continue with assigned database name: anh_production_data.db (REPLACED DATABASE RISK) :" )
answer = input()

if answer == '':
    print("You have decided to procced with default name: anh_production_data.db, thanks and enjoy your Data Mining ...")
    conn = sql.connect('anh_production_data.db')
    production_df.to_sql('anh_production_data', conn, if_exists='replace')
    answer = 'anh_production_data'
else : 
    print("Succesfully database creation as:  <<", answer, ".db>> thanks and enjoy your Data Mining ...")

conn = sql.connect(answer+'.db')
production_df.to_sql(answer, conn, if_exists='replace')




