from stockmanage.models import Product
from stockmanage.tools.read_excel_to_list import excel_reader
class importer:
    def __init__(self,excel_file_path):
        self.excel_file_path=excel_file_path
    
    def save_to_db(self):
        bookdata=excel_reader(excel_file_path).read()
        for sheet in bookdata['sheetsdata']:
            for row in sheet['rowlist']:
                
        
    def save_single(cell_values):
        '''save list to database'''
        product,created=Product.objects.get_or_create(
                                      SerialNo=cell_values[0],
                                      Code_Original=cell_values[1],
                                      Code_Database=cell_values[2],
                                      NTSCode='',
                                      Name=cell_values[3],
                                      ModelNumber=cell_values[4],
                                      Specification=cell_values[5],
                                      Material=cell_values[6],
                                      Price=cell_values[7],
                                      Unit=cell_values[8],
                                      SupplierCode=cell_values[9],
                                      State=cell_values[10]
                                      )
        
            
        