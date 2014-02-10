from django.test import TestCase
from random import choice
from autofixture import  AutoFixture,generators
from stockmanage.models import  Product,Productlanguage
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
                                           ,generate_fk=True)
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
                                           ,generate_fk=True)
        theproductlanguage=fixtureProductlanguage.create(1)
        self.assertTrue(theproduct.GetName('en'))
        
    def testGetnameWithNoLanguageVersion(self):
        fixtureProduct=AutoFixture(Product)
        theproduct=fixtureProduct.create(1)[0]
       
        self.assertRaisesRegex(Exception, '.*',)    
        
        
