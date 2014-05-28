from django.test import TestCase
from random import choice
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from autofixture import  AutoFixture,generators
from stockmanage.models import  Product,StockLocation,ProductStock,ProductSnapshot,StockBill,StockBillDetail,CheckBill,CheckBillDetail
# Create your tests here.
class AFTest(TestCase):
    def testCreate(self):
        af_StockBill=AutoFixture(StockBill,generate_fk=True)
        bill=af_StockBill.create(1)

        import pdb;pdb.set_trace()
class CheckBillDetailMethodTests(TestCase):
    def test_GenerateStockDetail(self):
        ft_stockbill=AutoFixture(StockBill,generate_fk=True)
        stockbills=ft_stockbill.create(2)
        ft_cbd=AutoFixture(CheckBillDetail,generate_fk=True, field_values={'quantity':1,'realquantity':4})
        detail=ft_cbd.create(1)[0]
        #import pdb;pdb.set_trace()
        detail.GenerateStockDetail(stockbills[0],stockbills[1])
        self.assertEqual(1,stockbills[1].stockbilldetail_set.count())
        self.assertEqual(3,stockbills[1].stockbilldetail_set.all()[0].quantity)
        #cbd=ft_cbd.Check

class ProductMethodTests(TestCase):   
    def test_get_a_snapshot_of_given_time(self):
        import os; file.readlines()
        print('----------test_get_a_snapshot_of_given_time')
        fixtureProduct=AutoFixture(Product)
        theproduct=fixtureProduct.create(1)[0]
        self.assertEqual(0,  theproduct.productsnapshot_set.all().count())
        
        snapshot1=theproduct.Snapshot()
        snapshot2=theproduct.productsnapshot_set.all()[0]
        self.assertEqual(1,  theproduct.productsnapshot_set.all().count())
        '''AssertionError: <stockmanage.models.ProductSnapshot object at 0x02CC85D0> != <st
ockmanage.models.ProductSnapshot object at 0x02CCCDD0>'''
        print('code:'+snapshot1.Code_Original)
        self.assertEqual(snapshot1.Code_Original, snapshot2.Code_Original,type(snapshot1))
        #self.assertEqual(snapshot1, snapshot2,type(snapshot1))
        print('type:'+str(type(snapshot1.id)))
        print (str(snapshot1.id))
        print('type2:'+str(type(snapshot2.id)))
        #TIPS: UUID,string. when get from database, the uuid become string. but before saving to db, it;s uuid type. 
        self.assertEqual(str(snapshot1.id),str(snapshot2.id))
        print(snapshot1)
        
        print(theproduct.productsnapshot_set.all()[0])
        

class StockLocationTest(TestCase):
    def testLocationGetChildren(self):
        
        fixtureParent=AutoFixture(StockLocation)
        locationParent=fixtureParent.create(1)[0]
        fixture=AutoFixture(StockLocation,
                            field_values={"ParentLocation":locationParent},
                             generate_fk=True)
        locations=fixture.create(5)
        self.assertEqual(5,len( locationParent.GetChildren()))
    
    def testLocationGetProductStock(self):
        
        fixtureProduct=AutoFixture(Product)
        theproduct=fixtureProduct.create(1)[0]
        
        
        fixturelocation=AutoFixture(StockLocation,generate_fk=True)
        location=fixturelocation.create(1)[0]
        fixturestock=AutoFixture(ProductStock,field_values={'theproduct':theproduct},)
        stocks=fixturestock.create(5)
        for stock in stocks:
            stock.stocklocation=location
        
        self.assertEqual(len(location.productstock_set.all()),5)
        
class StockBillTest(TestCase):
    
        
    def testSaveBill(self):
        fixtureProduct=AutoFixture(Product,field_values={'Price':1})
        theproduct=fixtureProduct.create(1)[0]
        theproduct.Price=1
    
        fixtureLocation=AutoFixture(StockLocation,generate_fk=True,
                                    field_values={'LocationCode':'1.1'})
        location=fixtureLocation.create(1)[0]
        fixtureBill=AutoFixture(StockBill,generate_fk=True,field_values={'BillState':'applied'})
        bill=fixtureBill.create(1)[0]
        fixtureBillDetail=AutoFixture(StockBillDetail,generate_fk=True
                                      ,field_values={'stockbill':bill,'product':theproduct,'quantity':1
                                                     ,'location':location})
        detail=fixtureBillDetail.create(5)
        
        bill.save()
        print (bill.BillType)
        self.assertEqual(len(ProductStock.objects.all()),1)
        self.assertEqual(ProductStock.objects.all()[0].quantity,5)
        print ([ProductStock.objects.all()])
        self.assertEqual(bill.TotalAmount,5)
        
        
        bill.BillType='out'
        bill.save()
        
        print (bill.BillType)
        print ([ProductStock.objects.all()])
        self.assertEqual(len(ProductStock.objects.all()),1)
        self.assertEqual(ProductStock.objects.all()[0].quantity,0)
        self.assertEqual(bill.TotalAmount,5)

class InitImportTest(TestCase):
    def import_normal(self):
        pass
