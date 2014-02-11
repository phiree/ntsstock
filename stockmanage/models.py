from datetime import datetime
from django.db import models
from django_extensions.db.fields import UUIDField
from django.db.models.fields import CharField, DecimalField,IntegerField,DateTimeField,TextField,\
    Field
from django.db.models.fields.related import ForeignKey, ManyToManyField

class Product(models.Model):
    id=UUIDField(primary_key=True)
    CategoryCode=CharField(max_length=255)
    CreateTime=DateTimeField('CreateTime',blank=True)
    LastUpdateTime=DateTimeField()
    ModelNumber=CharField(max_length=255)
    SupplierCode=CharField(max_length=255)
    NTSCode=CharField(max_length=255)
    OrderAmountMin=DecimalField(max_digits=19,decimal_places=5)
    PriceOfFactory=CharField(max_length=255)
    ProductionCycle=DecimalField(max_digits=19,decimal_places=5)
    State=IntegerField(default=0)
    TaxRate=DecimalField(max_digits=19,decimal_places=5)
    PriceDate=CharField(max_length=255)
    PriceValidPeriod=CharField(max_length=255)
    MoneyType=CharField(max_length=255)
    ImageState=CharField(max_length=255)
    SyncState=IntegerField()
    SyncTime=DateTimeField()
    ProductCode=CharField(max_length=255)
    ModelNumber_Original=CharField(max_length=255)
   
    def GetName(self,language):
        languageset=self.productlanguage_set.all()
        matches=[x for x in languageset if x.Language==language]
        if len(matches)==0:
            
            raise Exception('product {0} has no  language {1} version, its invalid,they are:{2}'.format(self.id,language,[str(x)+'|' for x in languageset]))
        elif len(matches)>1:
            raise Exception('product  has more than one ('+self.id+') language versions, it is invalid')    
        else:
            return matches[0].Name
    def Snapshot(self):
        snapshot=ProductSnapshot()
        snapshot.theproduct=self
        snapshot.SnapshotTime=datetime.now()
        snapshot.CategoryCode=self.CategoryCode
        snapshot.CreateTime=self.CreateTime
        snapshot.LastUpdateTime=self.LastUpdateTime
        snapshot.ModelNumber=self.ModelNumber
        snapshot.SupplierCode=self.SupplierCode
        snapshot.NTSCode=self.NTSCode
        snapshot.OrderAmountMin=self.OrderAmountMin
        snapshot.PriceOfFactory=self.PriceOfFactory
        snapshot.ProductionCycle=self.ProductionCycle
        snapshot.State=self.State
        snapshot.TaxRate=self.TaxRate
        snapshot.PriceDate=self.PriceDate
        snapshot.PriceValidPeriod=self.PriceValidPeriod
        snapshot.MoneyType=self.MoneyType
        snapshot.ImageState=self.ImageState
        snapshot.SyncState=self.SyncState
        snapshot.SyncTime=self.SyncTime
        snapshot.ProductCode=self.ProductCode
        snapshot.ModelNumber_Original=self.ModelNumber
        for productlanguage in self.productlanguage_set.all:
            plsnap=ProductlanguageSnapshot()
            plsnap.theproductSnapshot=snapshot
            plsnap.Name=productlanguage.Name
            plsnap.PlaceOfDelivery=productlanguage.PlaceOfDelivery
            plsnap.PlaceOfOrigin=productlanguage.PlaceOfOrigin
            plsnap.ProductDescription=productlanguage.ProductDescription
            plsnap.ProductParameters=productlanguage.ProductParameters
            plsnap.Language=productlanguage.Language
        
    class Meta:
        db_table="product"
    def __str__(self):
        return self.GetName('en')#Productlanguage.LanguageChoices[0])
    
class ProductSnapshot(models.Model):
    '''keep a snapshot when it is modified'''
    theproductSnapshot=ForeignKey(Product)
    CategoryCode=CharField(max_length=255)
    CreateTime=DateTimeField('CreateTime',blank=True)
    LastUpdateTime=DateTimeField()
    ModelNumber=CharField(max_length=255)
    SupplierCode=CharField(max_length=255)
    NTSCode=CharField(max_length=255)
    OrderAmountMin=DecimalField(max_digits=19,decimal_places=5)
    PriceOfFactory=CharField(max_length=255)
    ProductionCycle=DecimalField(max_digits=19,decimal_places=5)
    State=IntegerField(default=0)
    TaxRate=DecimalField(max_digits=19,decimal_places=5)
    PriceDate=CharField(max_length=255)
    PriceValidPeriod=CharField(max_length=255)
    MoneyType=CharField(max_length=255)
    ImageState=CharField(max_length=255)
    SyncState=IntegerField()
    SyncTime=DateTimeField()
    ProductCode=CharField(max_length=255)
    ModelNumber_Original=CharField(max_length=255)


class Productlanguage(models.Model):
    id=UUIDField(primary_key=True)
    Memo=CharField(max_length=255)
    Name=CharField(max_length=255)
    PlaceOfDelivery=CharField(max_length=255)
    PlaceOfOrigin=CharField(max_length=255)
    ProductDescription=TextField()
    ProductParameters=TextField()
    Unit=CharField(max_length=255)
    LanguageChoices=[('en','en'),('zh','zh')]
    Language=CharField(max_length=2,choices=LanguageChoices,default='en')
    theproduct=ForeignKey(Product)
    def __str__(self):
        return self.Name+'-'+self.Language
    class Meta:
        db_table='productlanguage'
    
class ProductlanguageSnapshot(models.Model):
    Memo=CharField(max_length=255)
    Name=CharField(max_length=255)
    PlaceOfDelivery=CharField(max_length=255)
    PlaceOfOrigin=CharField(max_length=255)
    ProductDescription=TextField()
    ProductParameters=TextField()
    Unit=CharField(max_length=255)
    LanguageChoices=[('en','en'),('zh','zh')]
    Language=CharField(max_length=2,choices=LanguageChoices,default='en')
    theproduct=ForeignKey(ProductSnapshot)
    
class ProductStock(models.Model):
    '''current stock quantity of a product
    
    '''
    Qty=IntegerField()
    theproduct=ForeignKey(Product)
    productSnapshot=ForeignKey(ProductSnapshot,null=True)
    #Redundancy of stocked product information
    productname=CharField(max_length=255)
    def __str__(self):
        return str(self.theproduct)+':'+str(self.Qty)
    
    

class StockLocation(models.Model):
    '''location infomation in the warehouse'''
    LocationCode=CharField(max_length=20)
    Description=CharField(max_length=200)
    ParentLocation=ForeignKey('self',db_column='parentlocation',blank=True,null=True)
    Products_Stocks=ManyToManyField(ProductStock)
    def __str__(self):
        return self.LocationCode
    def GetChildren(self):
        return self.stocklocation_set.all()#StockLocation.objects.filter(ParentLocation=self)





    
    
