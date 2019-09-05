# -*- coding: utf-8 -*-
import encodings
# https://xlsxwriter.readthedocs.io/
# The following library must be download and installed in order for this tool to work well
# https://xlsxwriter.readthedocs.io/getting_started.html
import xlsxwriter



class Excel:
#---------------------------------------------------------------------------- 
     def __init__(this, FileName,FileType,DatabaseName):
          this.FileName = FileName
          this.FileType = FileType
          this.DatabaseName = DatabaseName
          this.RowNo = 2
          this.ColumnNo = 1
          #------------------------------------------------------------------
          # Create Excel file
          this.workbook = xlsxwriter.Workbook(FileName)
          #print("workbook")
          # Create Sheets

          this.SheetFeatureClasses = this.workbook.add_worksheet('Feature Classes')
          this.SheetBusinessTable = this.workbook.add_worksheet('Business Table')

          #------------------------------------------------------------------
          # Create Header Style
          this.Header_Style = this.workbook.add_format()         
          this.Header_Style.set_bg_color('#434337') 
          this.Header_Style.set_border(1)
          this.Header_Style.set_bold()
          this.Header_Style.set_font_color('#FFFFFF')
          this.Header_Style.set_font_size(13)
          this.Header_Style.set_align('vcenter')
          this.Header_Style.set_text_wrap()
          #------------------------------------------------------------------
          # Create Main Style
          this.Main_Style = this.workbook.add_format()
          this.Main_Style.set_border(1)
          this.Main_Style.set_bold()
          this.Main_Style.set_font_size(12)
          this.Main_Style.set_align('vcenter')
          this.Main_Style.set_text_wrap()
          #------------------------------------------------------------------
          # Create Body Style
          this.Body_Style = this.workbook.add_format()
          this.Body_Style.set_border(1)
          this.Body_Style.set_align('vcenter')
          this.Body_Style.set_text_wrap()
          # Create All Headers
          this.CreateHeaders()
          
          #------------------------------------------------------------------
          # End of __init__ Function
#----------------------------------------------------------------------------
     def GetExcel(this):
          return this
#----------------------------------------------------------------------------  
     def SaveExcel(this):
          this.workbook.close()
#---------------------------------------------------------------------------- 
     def GetStyle(this,StyleNO):
          MyStyle = this.Body_Style
          if StyleNO == 1:               
               MyStyle = this.Header_Style
          elif StyleNO == 2:
               MyStyle = this.Main_Style
          elif StyleNO == 3:
               StyleNO = this.Body_Style
          return MyStyle
#---------------------------------------------------------------------------- 
     def Getworksheet(this,SheetNo):
          MySheet = this.SheetFeatureClasses
          if SheetNo == 1:              
               MySheet = this.SheetFeatureClasses
          elif SheetNo == 2:
               MySheet = this.SheetBusinessTable
      
          return MySheet
#----------------------------------------------------------------------------
     def Write(this,row, col,Value,SheetNo,StyleNO):
          MyStyle = this.GetStyle(StyleNO)
          MySheet = this.Getworksheet(SheetNo)
          #print("write value")
          MySheet.write(row, col,Value.decode("cp1256"),MyStyle)
          #MySheet.write(row, col,Value,MyStyle)
#----------------------------------------------------------------------------
     def merge_range(this,FristRow, FristCol,LastRow, LastCol,SheetNo,StyleNO,value):
          MySheet = this.Getworksheet(SheetNo)
          MyStyle = this.GetStyle(StyleNO)
          MySheet.merge_range(FristRow, FristCol, LastRow, LastCol,value.decode("cp1256"), MyStyle)
          #----------------------------------------------------------------------------
     def SetColumnWidth(this,FristColumn,LastColumn,Width,SheetNo):
          MySheet = this.Getworksheet(SheetNo)
          MySheet.set_column(FristColumn,LastColumn,Width)
#----------------------------------------------------------------------------
     def CreateHeaders(this):
          this.CreateFeatureClassesHeaders()
          this.CreateBusinessTableHeaders()   
#----------------------------------------------------------------------------
     def CreateFeatureClassesHeaders(this):
          SheetNo = 1
          this.Write(1, 1,"DataSet",SheetNo,1)          
          this.Write(1, 2,"Feature Classes",SheetNo,1)
          this.Write(1, 3,"New layer",SheetNo,1)
          this.Write(1, 4,"Geometry",SheetNo,1)  
          this.SetColumnWidth(0,0,2,SheetNo)
          this.SetColumnWidth(1,2,33,SheetNo)
          this.SetColumnWidth(3,3,45,SheetNo)
          this.SetColumnWidth(4,4,20,SheetNo)
 

#----------------------------------------------------------------------------
     def CreateBusinessTableHeaders(this):
          SheetNo = 2

          this.Write(1, 1,"Table Name",SheetNo,1) 
          this.Write(1, 2,"New Name",SheetNo,1)         

          this.SetColumnWidth(0,0,2,SheetNo)
          this.SetColumnWidth(1,3,40,SheetNo)

 #----------------------------------------------------------------------------
          
