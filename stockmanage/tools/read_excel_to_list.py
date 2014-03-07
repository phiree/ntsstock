import xlrd
import os
class excel_reader:
    def __init__(self,excel_file_path):
        self.excel_file_path=excel_file_path
        
    def read(self):
        workbook = xlrd.open_workbook(self.excel_file_path,formatting_info=True)
        worksheets=workbook.sheets()
        bookdata={}
        bookdata['filename']=self.excel_file_path
        bookdata['sheetsdata']=[]
        for sheet in worksheets:
            
            #fill merged cell with value of top left cell
            
            sheetdata={}
            sheetname=sheet.name
            sheetdata['sheetname']=sheetname
            sheetdata['rowlist']=[]
            current_row=0
            #print('sheet.nrows:'+str(sheet.nrows))
            #print('sheet.ncols:'+str(sheet.ncols))
            
            while current_row<sheet.nrows:
                rowdata=[]
                row=sheet.row(current_row)
                current_col=0
                #print('sheet.row_len():'+str(current_row)+','+str(sheet.row_len(current_row)))
                while current_col <sheet.ncols:
                    current_cell_value=sheet.cell_value(current_row,current_col)
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
        
        print('--------------------')
        for crange in sheet.merged_cells:
            print(crange)
            #0,1,0,3 the hi index is based 1 but the low 0, confused, bug?
            rlo, rhi, clo, chi = crange
            if rlo<=idxr<=rhi-1 and clo<=idxc<=chi-1: 
                return sheet.cell_value(rlo,clo)
        return ''
            
if __name__=='__main__':
    reader=excel_reader('test2.xls')
    print(reader.read())