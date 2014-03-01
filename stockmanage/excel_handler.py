import xlwt3 as xlwt
from datetime import datetime
class excel_writer():
    def __init__(self,objectlist,fieldlist,title):
        self.objectlist=objectlist
        self.fieldlist=fieldlist
        self.title=title
    def write(self): 
        wb = xlwt.Workbook()
        ws = wb.add_sheet(self.title)
        for idxobj,obj in enumerate(self.objectlist):
            print (obj)
            #import pdb;pdb.set_trace()
            for idxfld,field in enumerate(self.fieldlist):
                if idxobj==0:
                    ws.write(idxobj,idxfld,field)
                val=str(getattr(obj,field))
                ws.write(idxobj+1,idxfld,val)
        return wb
if __name__=='__main__':
    list=[{'field1':1,'field2':2},{'field1':11,'field22':22}]
    excel_writer(list,['field1'],'haha').wirte()
    print(wb)
    