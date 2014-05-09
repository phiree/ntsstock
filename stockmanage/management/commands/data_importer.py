
from stockmanage.models import Product,StockBill,StockBillDetail,ProductStock,StockLocation
from .read_excel_to_list import excel_reader
import re

class importer:
    def __init__(self,excel_file_path):
        
        self.excel_file_path=excel_file_path
    
    def save_to_db(self):
        bookdata=excel_reader(self.excel_file_path).read()
        #create a import bill for the init
        
        for sheet in bookdata['sheetsdata']:
            
            self.sheetname=sheet['sheetname']
            print('-----------------------------')
            print ('开始导入--'+self.sheetname)
            print('-----------------------------')
            for row in sheet['rowlist']:
                self.save_single(row)
                print(row[0])
            print('-----------------------------')
            print ('导入完毕--'+self.excel_file_path+'----'+self.sheetname)
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
        cell_price=row[7]
        try:
            cell_price=decimal(row[7])
        except:
            usd_re=re.match(r'usd(?P<dollar>\d+(\.\d+)?)',str(row[7]),re.I)
            if usd_re:
                try:
                    cell_price=decimal( usd_re.match('dollar'))
                except:
                    cell_price=0
            else:
                cell_price=0
        serialNo=row[0]
        if not serialNo:
            serialNo=0       
        #import pdb;pdb.set_trace()
        product,created=Product.objects.get_or_create(
                                      SerialNo=serialNo,
                                      Code_Original=row[1],
                                      Code_Database=row[2],
                                      NTSCode='',
                                      Name=row[3],
                                      ModelNumber=row[4],
                                      Specification=row[5],
                                      Material=row[6],
                                      Price=cell_price,
                                      Unit=row[8],
                                      SupplierCode=self.sheetname,
                                      #State=row[10] if row[10] else 0
                                      )
        #save productstock
        quantity=0
        try:
            quantity=int(row[11] if row[11] else row[10])
        except:
            quantity=0
        locationCode=str(row[13])
        locations=self.parse_location(locationCode)
        parent=None
        location=None
        if locations:
            for strlocation in locations:
                l,created=StockLocation.objects.get_or_create(LocationCode=strlocation,
                                                               Name=strlocation,
                                                               Description=strlocation,
                                                               ParentLocation=parent,
                                                               )
                parent=l
            location=StockLocation.objects.get(LocationCode=locationCode)
        ProductStock.objects.get_or_create(quantity=quantity,theproduct=product,stocklocation=location,memo=locationCode)
    def parse_location(self,location_code):
        #1.2.3-->1,1.2,1.3
        import re
        
        reg='^\d+\.\d+\.\d+$'
        r=re.compile(reg)
        #print(location_code)
        if not r.match(location_code.strip()):
            return []
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

        
    
        
                  
        
            
        
        
            
        