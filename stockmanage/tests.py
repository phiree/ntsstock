from django.test import TestCase
from random import choice
from django.utils import timezone
import datetime
from autofixture import  AutoFixture,generators
from stockmanage.models import  Product\
                        ,StockLocation,ProductStock,ProductSnapshot\
                        ,StockBill,StockBillDetail
# Create your tests here.
class CheckMethodTests(TestCase):
	def test_Complete_Check(self):
		fixtureProduct=AutoFixture(Product)
        theproduct=fixtureProduct.create(1)[0]
        fixtureParent=AutoFixture(StockLocation)
        locationParent=fixtureParent.create(1)[0]
        ProductStock.objects.create(Quantity=1,theproduct=theproduct,stocklocation=locationParent)
        
        checkbill=CheckBill.objects.create()
        checkbill.checkbilldetail_set.create()

class ProductMethodTests(TestCase):   
    def test_get_a_snapshot_of_given_time(self):
        
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
                                      ,field_values={'stockbill':bill,'product':theproduct,'Quantity':1
                                                     ,'location':location})
        detail=fixtureBillDetail.create(5)
        
        bill.save()
        print (bill.BillType)
        self.assertEqual(len(ProductStock.objects.all()),1)
        self.assertEqual(ProductStock.objects.all()[0].Quantity,5)
        print ([ProductStock.objects.all()])
        self.assertEqual(bill.TotalAmount,5)
        
        
        bill.BillType='out'
        bill.save()
        
        print (bill.BillType)
        print ([ProductStock.objects.all()])
        self.assertEqual(len(ProductStock.objects.all()),1)
        self.assertEqual(ProductStock.objects.all()[0].Quantity,0)
        self.assertEqual(bill.TotalAmount,5)
        