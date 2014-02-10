from django.db import models
from django_extensions.db.fields import UUIDField
from django.db.models.fields import CharField, DecimalField,IntegerField,DateTimeField,TextField,\
    Field
from django.db.models.fields.related import ForeignKey
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
            raise Exception('product {0} has no  language version, its invalid'.format(self.id))
        elif len(matches)>1:
            raise Exception('product  has more than one ('+self.id+') language versions, it is invalid')    
        else:
            return matches[0].Name
        
    class Meta:
        db_table="product"
    def __str__(self):
        return self.id

class Productlanguage(models.Model):
    id=UUIDField(primary_key=True)
    Memo=CharField(max_length=255)
    Name=CharField(max_length=255)
    PlaceOfDelivery=CharField(max_length=255)
    PlaceOfOrigin=CharField(max_length=255)
    ProductDescription=TextField()
    ProductParameters=TextField()
    Unit=CharField(max_length=255)
    Language=CharField(max_length=255)
    theproduct=ForeignKey(Product)
    def __str__(self):
        return self.Name
    class Meta:
        db_table='productlanguage'

class ProductStock(models.Model):
    Qty=IntegerField(default=0)
    theproduct=ForeignKey(Product)

    




    
    
