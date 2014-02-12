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
        theproductlanguage=fixtureProductlanguage.create(2)
        
        snapshot1=theproduct.Snapshot()
        print([snapshot1.productlanguagesnapshot_set.all()])
        '''snapshot1.ShotTime=timezone.now()+datetime.timedelta(days=1)
        snapshot2=theproduct.Snapshot()
        snapshot2.ShotTime=timezone.now()
        snapshot3=theproduct.Snapshot()
        snapshot3.ShotTime=timezone.now()-datetime.timedelta(days=1)'''
        print('snapshot amounts:'+str(theproduct.productsnapshot_set.all().count()))
        onesnapshot=theproduct.productsnapshot_set.all()[0]
        print(onesnapshot.id)
        print(onesnapshot.productlanguagesnapshot_set.all().count())
        print([onesnapshot.productlanguagesnapshot_set.all()])
        nearestSnap=theproduct.GetSnapshot(timezone.now())
        print(nearestSnap)
       
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
        print('id of product:'+theproduct.id)
        snapshot= theproduct.Snapshot()
        
        print(snapshot.theproduct.id)
        self.assertEqual(theproduct.CategoryCode, snapshot.CategoryCode)
        
        c=snapshot.productlanguagesnapshot_set.all().count()
        
        self.assertEqual(2, c)
        self.assertEqual(theproduct.productlanguage_set.all().count(), c)
        self.assertEqual(theproduct.productlanguage_set.first().Name,snapshot.productlanguagesnapshot_set.first().Name)
        
  
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
        
  
        
