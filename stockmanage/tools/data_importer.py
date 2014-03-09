from stockmanage.models import Product,StockBill,StockBillDetail,ProductStock
from stockmanage.tools.read_excel_to_list import excel_reader
class importer:
    def __init__(self,excel_file_path):
        self.excel_file_path=excel_file_path
    
    def save_to_db(self):
        bookdata=excel_reader(excel_file_path).read()
        #create a import bill for the init
        for sheet in bookdata['sheetsdata']:
            for row in sheet['rowlist']:
                save_single(row)
        
    def save_single(row):
        '''save list to database'''
        #save product info
        product,created=Product.objects.get_or_create(
                                      SerialNo=row[0],
                                      Code_Original=row[1],
                                      Code_Database=row[2],
                                      NTSCode='',
                                      Name=row[3],
                                      ModelNumber=row[4],
                                      Specification=row[5],
                                      Material=row[6],
                                      Price=row[7],
                                      Unit=row[8],
                                      SupplierCode=row[9],
                                      State=row[10]
                                      )
        #save productstock
        quantity=int(row[11] if row[11].strip() else row[10])
        locationCode=row[13]
        location=StockLocation.objects.get(LocationCode=locationCode)
        ProductStock(Quantity=quantity,theproduct=product,location=location).save()
        
    def parse_location(self,location_code):
        
        
                  
        
            
        
        
            
        