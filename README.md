# spe-hackaton2020
Participation in SPE Colombia 2020 

Nov 04th, 2020

Based on SPE-Guidelines 1st delivery focus on read_and_proccess.py file 

This file is able to read & proccess excel files from local machine (passed as arguments) or directly from ANH web page if "auto" reserved word is passed as argument

Example for running read_and_proccess.py script 

LOCAL EXCELS FILES IN YOUR MACHINE 
_____________________________________________________________

$python read_and_process.py FILE1.xlsx FILE2.xlsx FILE3.xlsx

_____________________________________________________________


TO ACCESS FILES FROM ANH WEB PAGE 
______________________________________________________________
$python read_and_process.py auto 
______________________________________________________________

This Script will run over excel files and has 3 main objectives:
- Look for year inside header of excel file 
- Identify header / footage structure and columns name and row index for parse 
- Load data to a pandas Data Frame 

One additional requirement at the end of this Script is save it to a SQL database. You will be ask for a name to this database, if no name is entered default database name is as follow: 'anh_production_data.db' 


Thanks for review and using this file, don't hesitate to contact me if some support or bug is noticed 


German Barboza on Nov 4th of 2020 


