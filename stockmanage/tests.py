from django.test import TestCase
from random import choice
from django.utils import timezone
import datetime
from autofixture import  AutoFixture,generators
from stockmanage.models import  Product,Productlanguage,StockLocation,ProductStock,ProductSnapshot,ProductlanguageSnapshot
# Create your tests here.
class ProductMethodTests(TestCase):
    
    def testGetnameWithMoreThanOneLanguageVersion(self):
        fixtureProduct=AutoFixture(Product)
        theproduct=fixtureProduct.create(1)[0]
        fixtureProductlanguage=AutoFixture(Productlanguage,
                                           field_values={
                                                         'Language':'en',
                                                         'theproduct':theproduct
                                                         }
                                           ,)
        theproductlanguage=fixtureProductlanguage.create(11)
        self.assertRaisesRegex(Exception, '.*',)        
        
    def testGetnameWithOneLanguageVersion(self):
        fixtureProduct=AutoFixture(Product)
        theproduct=fixtureProduct.create(1)[0]
        fixtureProductlanguage=AutoFixture(Productlanguage,
                                           field_values={
                                                         'Language':'en',
                                                         'theproduct':theproduct
                                                         }
                                           ,)
        theproductlanguage=fixtureProductlanguage.create(1)
        self.assertTrue(theproduct.GetName('en'))
        
    def testGetnameWithNoLanguageVersion(self):
        fixtureProduct=AutoFixture(Product)
        theproduct=fixtureProduct.create(1)[0]
        self.assertRaisesRegex(Exception, '.*',)
    def test_get_a_snapshot_of_given_time(self):
        
        print('----------test_get_a_snapshot_of_given_time')
        fixtureProduct=AutoFixture(Product)
        theproduct=fixtureProduct.create(1)[0]
        fixtureProductlanguage=AutoFixture(Productlanguage,
                                           field_values={
                                                         'Language':'en',
                                                         'theproduct':theproduct
                                                         }
                                           ,)
        theproductlanguage=fixtureProductlanguage.create(1)
        #造像
        self.assertEqual(0,  theproduct.productsnapshot_set.all().count())
        
        snapshot1=theproduct.Snapshot()
        snapshot2=theproduct.productsnapshot_set.all()[0]
        self.assertEqual(1,  theproduct.productsnapshot_set.all().count())
        '''AssertionError: <stockmanage.models.ProductSnapshot object at 0x02CC85D0> != <st
ockmanage.models.ProductSnapshot object at 0x02CCCDD0>'''
        print('CateCode:'+snapshot1.CategoryCode)
        self.assertEqual(snapshot1.CategoryCode, snapshot2.CategoryCode,type(snapshot1))
        #self.assertEqual(snapshot1, snapshot2,type(snapshot1))
        print('type:'+str(type(snapshot1.id)))
        print (str(snapshot1.id))
        print('type2:'+str(type(snapshot2.id)))
        #TIPS: UUID,string. when get from database, the uuid become string. but before saving to db, it;s uuid type. 
        self.assertEqual(str(snapshot1.id),str(snapshot2.id))
        print(snapshot1)
        
        print(theproduct.productsnapshot_set.all()[0])
        
    def test_make_a_snapshot(self):
        print('-----test_make_a_snapshot--------')
        fixtureProduct=AutoFixture(Product)
        theproduct=fixtureProduct.create(1)[0]
        fixtureProductlanguage=AutoFixture(Productlanguage,
                                           field_values={
                                                         'Language':'en',
                                                         'theproduct':theproduct
                                                         }
                                           ,)
        theproductlanguage=fixtureProductlanguage.create(2)
        snapshot= theproduct.Snapshot()
        snapshotInProduct=theproduct.productsnapshot_set.all()[0]
        self.assertEqual(sorted([x.Name for x in theproduct.productlanguage_set.all()]),
                         sorted([x.Name for x in snapshot.productlanguagesnapshot_set.all()]))
        self.assertEqual(theproduct.CategoryCode,snapshot.CategoryCode)
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
        fixtureProductlanguage=AutoFixture(Productlanguage,
                                           field_values={
                                                         'Language':'en',
                                                         'theproduct':theproduct
                                                         }
                                           ,)
        theproductlanguage=fixtureProductlanguage.create(1)
        
        fixturelocation=AutoFixture(StockLocation,generate_fk=True)
        locations=fixturelocation.create(5)
        fixturestock=AutoFixture(ProductStock,field_values={'theproduct':theproduct},)
        stocks=fixturestock.create(5)
        print('------stock in location-------')
        for location in locations:
            location.Products_Stocks=stocks
            print(len(location.Products_Stocks.all()))
            pass
            #location.ProductStocks=stocks
        print('------location in stock-------')
        for stock in stocks:
            stock.Products_Stocks=locations
           
            print(len(stock.Products_Stocks))
        print('------stocks in one location of '+str(locations[0]))
        for stock in locations[0].Products_Stocks.all():
            print(stock)
        
  
        
