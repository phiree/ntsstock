import xlrd
import os
from datetime import datetime
class excel_reader:
    def __init__(self,excelcontent):
        self.excelcontent=excelcontent
        
    def read(self):
        workbook = xlrd.open_workbook(file_contents=self.excelcontent,formatting_info=True)
        worksheets=workbook.sheets()
        bookdata={}
        bookdata['filename']='dd'
        bookdata['sheetsdata']=[]
        for sheet in worksheets:
            
            #fill merged cell with value of top left cell
            
            sheetdata={}
            sheetname=sheet.name
            sheetdata['sheetname']=sheetname
            sheetdata['rowlist']=[]
            current_row=3 # skip the title
            #print('sheet.nrows:'+str(sheet.nrows))
            #print('sheet.ncols:'+str(sheet.ncols))
            
            while current_row<sheet.nrows:
                
                rowdata=[]
                row=sheet.row(current_row)
                dud_types = set([xlrd.XL_CELL_BLANK, xlrd.XL_CELL_EMPTY ]) 
                rowf = [ ty for ty in sheet.row_types(sheet.nrows-1) ] 
                if all( x in dud_types for x in rowf ): 
                    current_row+=1
                    continue
    
                current_col=0
                #print('sheet.row_len():'+str(current_row)+','+str(sheet.row_len(current_row)))
                while current_col <sheet.ncols:
                    current_cell_value=sheet.cell_value(current_row,current_col)
                    current_cell_type=sheet.cell_type(current_row,current_col)
                    if current_cell_type== xlrd.XL_CELL_DATE:
                            dt_tuple = xlrd.xldate_as_tuple(current_cell_value, workbook.datemode)
                            # Create datetime object from this tuple.
                            get_col = datetime(
                            dt_tuple[0], dt_tuple[1], dt_tuple[2], 
                            dt_tuple[3], dt_tuple[4], dt_tuple[5]
                            )
                    
                    if current_cell_value=='':
                        current_cell_value=self.get_value_for_merged_cell(sheet, current_row,current_col)
                    #print ('current_row:'+str(current_row)+'current_col:'+str(current_col)+'value:'+str(current_cell_value))
                    
                    rowdata.append(current_cell_value)
                    current_col+=1
                current_row+=1
                pass
                sheetdata['rowlist'].append(rowdata)
            bookdata['sheetsdata'].append(sheetdata)
        return bookdata
    
    def get_value_for_merged_cell(self,sheet,idxr,idxc):
        #import pdb;pdb.set_trace()
        
        #print('--------------------')
        for crange in sheet.merged_cells:
            #print(crange)
            #0,1,0,3 the hi index is based 1 but the low 0, confused, bug?
            rlo, rhi, clo, chi = crange
            if rlo<=idxr<=rhi-1 and clo<=idxc<=chi-1: 
                return sheet.cell_value(rlo,clo)
        return ''
            
if __name__=='__main__':
    reader=excel_reader('test.xls')
    print(reader.read())