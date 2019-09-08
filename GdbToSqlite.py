# -*- coding: utf-8 -*-
from __future__ import print_function
import encodings
import  datetime,gc
import sys ,os ,arcpy
import sqlite3
from time import strftime
import time
from functools import wraps
#----------------------------------------------------------------------------


class GdbToSqlite:
#---------------------------------------------------------------------------- 

     def report_time(func):
          '''Decorator reporting the execution time'''
          @wraps(func)
          def wrapper(*args, **kwargs):
               start = time.time()
               result = func(*args, **kwargs)
               end = time.time()
               print(func.__name__, round(end-start,3))
               return result
          return wrapper
#----------------------------------------------------------------------------
     @report_time
     def __init__(this, workspace ,convertType):

          arcpy.env.workspace =str(workspace.encode("cp1256")) 
          workspacedesc = arcpy.Describe(arcpy.env.workspace)
          Database= str(workspace.encode("cp1256")).split('\\')[-1:][0]
          FileType =str(workspacedesc.workspaceType).encode("cp1256")

          workspaceEncoding= str(workspace.encode("cp1256")).decode("cp1256") 
          filePath = str(os.path.dirname(workspaceEncoding.encode("cp1256"))).decode("cp1256") 
          NewDbName = filePath + "\\"
          NewDbName = NewDbName + Database.decode("cp1256").rsplit( ".", 1 )[ 0 ] + strftime("%Y%m%d_%H%M%S")
          gdb = workspace 
          

          extension = '.gpkg'
          if convertType == 'OGC Sqlite':               
               extension = '.sqlite'
               NewDbName = NewDbName + extension
          elif convertType =='Geo Package':
               extension = '.gpkg'
               NewDbName = NewDbName + extension 
               arcpy.CreateSQLiteDatabase_management(NewDbName, 'GEOPACKAGE')
           
          print(NewDbName)         
          this.conn = sqlite3.connect(NewDbName)
          this.convertType = convertType
          this.NewDbName = NewDbName          
          this.workspace = arcpy.env.workspace
          this.extension = extension
          this.conn = this.enable_spatial()

          #------------------------------------------------------------------
          # End of __init__ Function

#----------------------------------------------------------------------------
     #@report_time
     def enable_spatial(this):
          #allow loading extensions
          this.conn.enable_load_extension(True)
          #loading the ST_Geometry dll to support Esri ST_Geometry geometry type
          #-----------------------------------------------------------------
          dll_path = r'c:\Program Files (x86)\ArcGIS\Desktop10.6\DatabaseSupport\SQLite\Windows32\stgeometry_sqlite.dll'
          this.run('''SELECT load_extension('{dll_path}','SDE_SQL_funcs_init');'''.format(dll_path=dll_path))
          if this.convertType == 'OGC Sqlite':               
               this.run('''SELECT CreateOGCTables();''')
          elif this.convertType =='Geo Package':
               this.run('''SELECT CreateGpkgTables()''')
          #-----------------------------------------------------------------
          this.conn.commit() 
          return this.conn
          
#----------------------------------------------------------------------------
     #@report_time
     def run(this,SQL=None):
          return this.conn.execute(SQL).fetchall()


#----------------------------------------------------------------------------
     #@report_time
     def featureClassToSqlite(this,source_fc,DataSetName=None):
          #conn = this.conn
          if DataSetName != '':
               DataSetName = DataSetName +"_";
          '''load a gdb feature class into a sqlite table with ST_Geometry type'''          
          #this.conn = this.enable_spatial()

          source_epsg = arcpy.Describe(source_fc).spatialReference.factoryCode
          source_basename = arcpy.Describe(source_fc).baseName
          source_shapetype = arcpy.Describe(source_fc).shapeType
          source_oid = arcpy.Describe(source_fc).OIDFieldName
          LayerName = source_basename
          if DataSetName != '':
               LayerName = DataSetName + source_basename;

          arcgis_sqlite_types_mappings = {'Date':'realdate','Double':'float64','Single':'float64',
                                             'Integer':'int32','SmallInteger':'int16','String':'text',
                                             'OID':'int32'}

          arcgis_sqlite_geometry_mappings = {'Polyline':'MultiLinestring','Point':'Point',
                                             'Multipoint':'Multipoint','Polygon':'MultiPolygon'}

          geometry_columns = ('shape','shape_area','shape_length')

          #use SQL to create a table
          columns = ['{} {}'.format(field.name,arcgis_sqlite_types_mappings[field.type])
                         for field in arcpy.ListFields(source_fc) if field.name.lower() not in
                         geometry_columns]

          #creating the table (with all columns except the geometry column)
          this.run('''CREATE TABLE {table} ({columns});'''.format(table=LayerName,
                                                             columns=','.join(columns)))
 

          #adding the Shape column
          shape_type = arcgis_sqlite_geometry_mappings[source_shapetype]
          sql_add_geom_col = '''SELECT AddGeometryColumn(null,'{table}','Shape',{epsg_code},'{shape_type}','xy','null');'''
          this.run(sql_add_geom_col.format(table=LayerName,
                                        epsg_code=source_epsg,
                                        shape_type=shape_type))

          #getting a list of column names to store the data
          data_columns = [str(field.name) for field in arcpy.ListFields(source_fc)
                              if field.name.lower() not in geometry_columns]

          #creating a list of data rows (all attributes plus WKT of Shape)
          rows = (r for r in arcpy.da.SearchCursor(source_fc,data_columns+['SHAPE@WKT']))

          #insert attribute values into the SQL table
          shape_type='st_{}'.format(arcgis_sqlite_geometry_mappings[source_shapetype])
          insert_values = ','.join(['?' for i in xrange(len(data_columns))] +
                                   ['{shape_type}(?,{epsg})'.format(shape_type=shape_type,
                                                                      epsg=source_epsg)])

          sql_insert_rows = '''Insert into {table_name} ({columns}) values ({insert_values})'''
          this.conn.executemany(sql_insert_rows.format(table_name = LayerName,
                                                  columns = ','.join(data_columns+['Shape']),
                                                  insert_values=insert_values),rows)
          this.conn.commit()
          return this.conn, LayerName
          #return conn
          #return LayerName

#----------------------------------------------------------------------------
     #@report_time
     def BusinessTableToSqlite(this,source_tbl):

          source_basename = arcpy.Describe(source_tbl).baseName
          source_oid = arcpy.Describe(source_tbl).OIDFieldName
          LayerName = source_basename
          arcgis_sqlite_types_mappings = {'Date':'realdate','Double':'float64','Single':'float64',
                                             'Integer':'int32','SmallInteger':'int16','String':'text',
                                             'OID':'int32'}



          #use SQL to create a table
          columns = ['{} {}'.format(field.name,arcgis_sqlite_types_mappings[field.type])
                         for field in arcpy.ListFields(source_tbl) ]

          #creating the table (with all columns except the geometry column)
          this.run('''CREATE TABLE {table} ({columns});'''.format(table=LayerName,
                                                             columns=','.join(columns)))
          #print('''CREATE TABLE {table} ({columns});'''.format(table=LayerName, columns=','.join(columns)))
          this.conn.commit()                                     

          #getting a list of column names to store the data
          data_columns = [str(field.name) for field in arcpy.ListFields(source_tbl)]
          #creating a list of data rows (all attributes plus WKT of Shape)
          rows = (r for r in arcpy.da.SearchCursor(source_tbl,data_columns))
          insert_values = ','.join(['?' for i in xrange(len(data_columns))] )
          sql_insert_rows = '''Insert into {table_name} ({columns}) values ({insert_values})'''
          #print(sql_insert_rows.format(table_name = LayerName,columns = ','.join(data_columns),insert_values=insert_values))
          this.conn.executemany(sql_insert_rows.format(table_name = LayerName, columns = ','.join(data_columns),insert_values=insert_values),rows)
                                 
          this.conn.commit()
          return this.conn, LayerName

          #return conn
          #return LayerName

#----------------------------------------------------------------------------
     @report_time
     def FirefeatureClass(this,featureClass,DataSetName):
          LayerName = ''          
          try:
               this.conn,LayerName = this.featureClassToSqlite( featureClass,DataSetName)
               source_basename = arcpy.Describe(featureClass).baseName
               print("succeeded convert layer: "+source_basename +" to: " + LayerName)                  
          except:
               print("Erorr while convert layer: "+str(featureClass.encode("cp1256")).decode("cp1256") )
               arcpy.AddMessage("Erorr while convert layer: " + str(featureClass.encode("cp1256")).decode("cp1256"))
          return LayerName
#----------------------------------------------------------------------------
     @report_time
     def FireBusinessTable(this,BusinessTable):
          LayerName = ''          
          try:
               this.conn,LayerName = this.BusinessTableToSqlite(BusinessTable)
               print("succeeded convert Table:1 "+str(BusinessTable.encode("cp1256")).decode("cp1256") +" to: " + LayerName) 
                 
          except:
               
               print("Erorr while convert Table: "+str(BusinessTable.encode("cp1256")).decode("cp1256") )
               arcpy.AddMessage("Erorr while convert Table: " + str(BusinessTable.encode("cp1256")).decode("cp1256"))
          return LayerName
#----------------------------------------------------------------------------
     def Close(this):
          this.conn.close()
          return this.NewDbName
          
          
#----------------------------------------------------------------------------
     def GetDbName(this):
          return this.NewDbName
#----------------------------------------------------------------------------
 
