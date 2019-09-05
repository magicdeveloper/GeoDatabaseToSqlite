
# GeoDatabaseToSqlite

GeoDatabaseToSqlite is a geospatial library to convert file GeoDatabase to sqlite geopackage
Developed by Mohamed Abdelgalil Ali Elghannam <magic_developer@hotmail.com>

## installation 
### First install dependency library 
install XlsxWriter Python library that manged Excel files

#### 1- open CMD command line and set Python path use next command
    set path=C:\Python27\ArcGIS10.6
Note : Replace the path and use yours path 
    
#### 2- download  and Extract  XlsxWriter Python library that manged Excel files 
XlsxWriter  from source  : https://github.com/jmcnamara/XlsxWriter.git
#### 3- Extract XlsxWriter  that you are downloaded and copy path
#### 3- open CMD command line and navigate to library path using next command
    cd C:\GeoDatabaseToSqlite\XlsxWriter
 Note : Replace the path and use yours path
 
#### 4- install  XlsxWriter  library  using next command
    python setup.py install
Congratulations you are now finished installing the library
  ![Congratulations you are now finished installing the library](https://github.com/magicdeveloper/GeoDatabaseToSqlite/blob/master/pic/cmd.PNG)
## next step
Download the current project on your PC from "Clone or download " button In the top right corner of current page

#### 1- open [GdbToSqlite.py](https://github.com/magicdeveloper/GeoDatabaseToSqlite/blob/master/GdbToSqlite.py) file and go to line 69 and replace the next code with your correct path and save it
    dll_path =  r'c:\Program Files (x86)\ArcGIS\Desktop10.6\DatabaseSupport\SQLite\Windows32\stgeometry_sqlite.dll'
#### 2- open _ArcCatalog_ and create new toolbox and right click and choose Add -> Script
![enter image description here](https://github.com/magicdeveloper/GeoDatabaseToSqlite/blob/master/pic/addscript.PNG)
 - ##### set script name as you which and  click  next 
![enter image description here](https://github.com/magicdeveloper/GeoDatabaseToSqlite/blob/master/pic/addscript1.PNG)
 - ##### set script file to [Main.py](https://github.com/magicdeveloper/GeoDatabaseToSqlite/blob/master/Main.py) and  click  next 
 ![enter image description here](https://github.com/magicdeveloper/GeoDatabaseToSqlite/blob/master/pic/addscript2.PNG)
-  ##### add two input parameters to tool

- The first parameter name "database'' and datatype is "workspace"

- The second parameter name "convert type'' and datatype is ''String''

   - add two items in filter list in "convert type'' parameter ['OGC Sqlite','Geo Package']

![like this](https://github.com/magicdeveloper/GeoDatabaseToSqlite/blob/master/pic/parameters.PNG)

##
**End**

