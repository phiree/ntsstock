import xlrd
import os
class excel_reader:
    def __init__(self,excel_file_path):
        self.excel_file_path=excel_file_path
        
    def read(self):
        workbook = xlrd.open_workbook(self.excel_file_path)
        worksheets=workbook.sheets()
        for sheet in worksheets:
            sheetname=sheet.name
            current_row=0
            print('sheet.nrows:'+str(sheet.nrows))
            print('sheet.ncols:'+str(sheet.ncols))
            while current_row<sheet.nrows:
                row=sheet.row(current_row)
                current_col=0
                print('sheet.row_len():'+str(current_row)+','+str(sheet.row_len(current_row)))
                while current_col <sheet.ncols:
                    print ('current_row:'+str(current_row)+'current_col:'+str(current_col)+'value:'+str( sheet.cell_value(current_row,current_col)))
                    current_col+=1
                current_row+=1
                pass
if __name__=='__main__':
    reader=excel_reader('test2.xlsx')
    reader.read()