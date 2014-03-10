
from stockmanage.models import Product,StockBill,StockBillDetail,ProductStock,StockLocation
from .read_excel_to_list import excel_reader


class importer:
    def __init__(self,excel_file_path):
        self.excel_file_path=excel_file_path
    
    def save_to_db(self):
        bookdata=excel_reader(self.excel_file_path).read()
        #create a import bill for the init
        for sheet in bookdata['sheetsdata']:
            self.sheetname=sheet['sheetname']
            for row in sheet['rowlist']:
                self.save_single(row)
            print('-----------------------------')
            print (self.sheetname+'导入完毕')
            print('-----------------------------')
        
    def save_single(self,row):
        '''save list to database'''
        #save product info
        #import pdb;pdb.set_trace()
        if row[17]=='已退货':
            return
        if row[7]=='无此产品':
            return
        if row[7]=='':
            row[7]=0
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
                                      SupplierCode=self.sheetname,
                                      State=row[10]
                                      )
        #save productstock
        quantity=int(row[11] if row[11] else row[10])
        locationCode=row[13]
        locations=self.parse_location(locationCode)
        parent=None
        for strlocation in locations:
            l,created=StockLocation.objects.get_or_create(LocationCode=strlocation,
                                                           Name=strlocation,
                                                           Description=strlocation,
                                                           ParentLocation=parent)
            parent=l
        location=StockLocation.objects.get(LocationCode=locationCode)
        ProductStock.objects.get_or_create(Quantity=quantity,theproduct=product,stocklocation=location)
    def parse_location(self,location_code):
        #1.2.3-->1,1.2,1.3
        import re
        
        reg='^\d+\.\d+\.\d+$'
        r=re.compile(reg)
        #print(location_code)
        if not r.match(location_code.strip()):
            raise
        seperated= location_code.split('.')
        locations=[]
        base=''
        for s in seperated:
            #import pdb;pdb.set_trace()
            base+=s+'.'
            locations.append(base.rstrip('.'))
        return locations
if __name__=="__main__":

    importer('test-t.xls').save_to_db()

        
    
        
                  
        
            
        
        
            
        