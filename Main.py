# -*- coding: utf-8 -*-
import encodings
import os, sys,arcpy,datetime,gc
from Excel import *
from time import strftime
from GdbToSqlite import *
#---------------------------------------------------------------------------
arcpy.overWriteOutputs = 1
CurrentTime = datetime.datetime.now()
arcpy.env.overwriteOutput = True

#reload(sys)
#sys.setdefaultencoding('utf-8')  

#---------------------------------------------------------------------------
arcpy.AddMessage("Data Base converter Start wait Second.....")
print("Data Base converter Start wait Second.....")
workspace = arcpy.GetParameterAsText(0)
ConvertType = arcpy.GetParameterAsText(1)
#TAG_RE = re.compile(r'<[^>]+>')
#-----------------------------------------------------------------------------------
##try:
if workspace == '#' or not workspace:
     workspace =r"C:\D\KA\Project\SDI\SDI_v0.10_2019-07-20_SK.gdb"
if ConvertType == '#' or not ConvertType:
     ConvertType ='Geo Package'
arcpy.env.workspace =str(workspace.encode("cp1256")) 
workspacedesc = arcpy.Describe(arcpy.env.workspace)
workspaceEncoding= str(workspace.encode("cp1256")).decode("cp1256") 
arcpy.AddMessage('----------------------------------------')
print('----------------------------------------')
arcpy.AddMessage(workspaceEncoding)
#-----------------------------------------------------------------------------------
converter = GdbToSqlite(arcpy.env.workspace, ConvertType)
#-----------------------------------------------------------------------------------     

Database= str(workspace.encode("cp1256")).split('\\')[-1:][0]
FileType =str(workspacedesc.workspaceType).encode("cp1256")
if FileType == '#' or not FileType:
     FileType = r"GDB"
#-----------------------------------------------------------------------------------

filePath = str(os.path.dirname(workspaceEncoding.encode("cp1256"))).decode("cp1256") 
ExcelName = filePath + "\\"
ExcelName = ExcelName + Database.decode("cp1256").rsplit( ".", 1 )[ 0 ] +"_"+ strftime("%Y%m%d_%H%M%S") + ".xlsx"
#ExcelName = ExcelName +str(CurrentTime.year).encode("cp1256")+"-"+str(CurrentTime.month).encode("cp1256")+"-"+str(CurrentTime.day).encode("cp1256")+".xlsx"
arcpy.AddMessage(ExcelName)
print(ExcelName)
if ExcelName == '#' or not ExcelName:
     ExcelName = r"ExcelName.xlsx"
#print(ExcelName)
#-----------------------------------------------------------------------------------
xls = Excel(ExcelName,FileType,Database)
#-----------------------------------------------------------------------------------
ErorrsMSG = ""
ErrorCount = 0
FCRow = 2
FCCol = 1
BusinessTableRow = 2
BusinessTableCol = 1
BusTableFildesRow = 2
BusTableFildesCol = 1
FCSheet = 1
BusinessTableSheet = 2
FieldsCount = 0
#-----------------------------------------------------------------------------------
datasets = arcpy.ListDatasets("*", "Feature") + ['']
datasets.sort()
#-----------------------------------------------------------------------------------
arcpy.AddMessage('----------------------------------------')
arcpy.AddMessage('export DataSets')
print('------------export DataSets--------------')
#print('export DataSets')


#-----------------------------------------------------------------------------------

for dataset in datasets:
    DatasetName = str(dataset.encode("cp1256"))
    if len(DatasetName) < 1:
          DatasetName = "NonDataSet"
    arcpy.AddMessage(str(DatasetName).decode("cp1256"))
    print(str(DatasetName).decode("cp1256"))
    #----------------------------------------------------
    FeatureClassesList = arcpy.ListFeatureClasses("*","",dataset)
    FeatureClassesList.sort()
    if len(FeatureClassesList) > 1:
         FCCol = 1
         xls.merge_range(FCRow, FCCol,(FCRow + len(FeatureClassesList)-1), FCCol, FCSheet, 2, DatasetName)
         FCCol = FCCol + 1
         
    for fc in FeatureClassesList:
        FCCol = 2
        FCDesc = ""
        FCDescError = 0 
        try:
              FCDesc = arcpy.Describe(fc)
        except IOError:
              FCDescError = 1
              ErorrsMSG = ErorrsMSG +  "Error In Describe FeatureClass: " + str(fc.encode("cp1256")).decode("cp1256")+"\n"
              arcpy.AddMessage("Error In Describe FeatureClass: " + str(fc.encode("cp1256")).decode("cp1256"))
              print("Error In Describe FeatureClass: " + str(fc.encode("cp1256")).decode("cp1256"))
              #print ("Error In Describe FeatureClass: " + str(fc.encode("cp1256")).decode("cp1256"))
              ErrorCount = ErrorCount + 1
         
 
        arcpy.AddMessage(str('---------------------').decode("cp1256"))
        arcpy.AddMessage(str("DataSet: "+DatasetName + " --> Feature Class : " + fc.encode("cp1256")).decode("cp1256"))
        print(str("DataSet: "+DatasetName + " --> Feature Class : " + fc.encode("cp1256")).decode("cp1256"))

        if len(FeatureClassesList) < 2:
              FCCol = 1
              xls.Write(FCRow,FCCol,DatasetName,FCSheet,2)
              FCCol = FCCol + 1

        xls.Write(FCRow,FCCol,fc.encode("cp1256"),FCSheet,3)
        FCCol = FCCol + 1
        LayerName = converter.FirefeatureClass(fc,DatasetName);
        xls.Write(FCRow,FCCol,LayerName,FCSheet,3)
        #print(LayerName)
        FCCol = FCCol + 1
        if hasattr(FCDesc,'featureType'):
             xls.Write(FCRow,FCCol,FCDesc.shapeType,FCSheet,3)
        FCCol = FCCol + 1
        #FCCol = 2
        FCRow = FCRow + 1
        del FCDesc



    #-----------------------------------------------------------
    del FeatureClassesList

#-----------------------------------------------------------------------------------
 
#-----------------------------------------------------------------------------------
### Get and print a list of tables
##arcpy.AddMessage(str('-----------------------------------').decode("cp1256"))
##arcpy.AddMessage(str('Export Taples').decode("cp1256"))
##arcpy.AddMessage(str('-----------------------------------').decode("cp1256"))
###print('-----------------------------------')
###print('Export Taples')
###print('-----------------------------------')
##tables = arcpy.ListTables()
##for table in tables:
##     BusinessTableCol = 1
##     tablename = str(table.encode("cp1256")).decode("cp1256")
##     arcpy.AddMessage(tablename)
##     xls.Write(BusinessTableRow,BusinessTableCol,str(table.encode("cp1256")),BusinessTableSheet,3)
##     BusinessTableCol = BusinessTableCol + 1
##     #-----------------------------------
##     newDbname = converter.GetDbName()
##     #arcpy.TableToTable_conversion(tablename, newDbname, tablename)
##     #NewTableName = converter.FireBusinessTable(table);
##     xls.Write(BusinessTableRow,BusinessTableCol,tablename,BusinessTableSheet,3)
## 
##     #-----------------------------------
##     BusinessTableRow = BusinessTableRow + 1
##arcpy.AddMessage(str('-------------------------').decode("cp1256"))
###-----------------------------------------------------------------------------------
 
#-------------------------------------------------------------------------------------
 
#-------------------------------------------------------------------------------------
arcpy.env.workspace = filePath
xls.SaveExcel()
arcpy.AddMessage(str("Excel file saved").decode("cp1256"))
arcpy.AddMessage(str("Finsh").decode("cp1256"))
arcpy.AddMessage("Excel File location:") 
arcpy.AddMessage(ExcelName)

converter.Close()
del xls
del datasets
#del tables
del workspacedesc
#print("clear momery\n-----------------")
gc.collect()

 
 
 


