import uuid,time,logging
from django.contrib.auth.models import User
from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from django.db import models
from django_extensions.db.fields import UUIDField
from django.db.models.fields import CharField, DecimalField,IntegerField,DateTimeField,TextField,\
    Field
from django.db.models.fields.related import ForeignKey, ManyToManyField
logger = logging.getLogger(__name__)
class Product(models.Model):
    id=UUIDField(primary_key=True)
    CategoryCode=CharField(max_length=255)
    CreateTime=DateTimeField('CreateTime',blank=True,default=datetime.now())
    LastUpdateTime=DateTimeField(blank=True,default=datetime.now())
    ModelNumber=CharField(max_length=255)
    SupplierCode=CharField(max_length=255)
    NTSCode=CharField(max_length=255)
    OrderAmountMin=DecimalField(max_digits=10,decimal_places=2)
    PriceOfFactory=CharField(max_length=255,default='0')
    ProductionCycle=DecimalField(max_digits=10,decimal_places=2)
    State=IntegerField(default=0)
    TaxRate=DecimalField(max_digits=10,decimal_places=2)
    PriceDate=CharField(max_length=255)
    PriceValidPeriod=CharField(max_length=255)
    MoneyType=CharField(max_length=255)
    ImageState=CharField(max_length=255)
    SyncState=IntegerField(default=0)
    SyncTime=DateTimeField(blank=True,null=True)
    ProductCode=CharField(max_length=255)
    ModelNumber_Original=CharField(max_length=255)
   
    def GetName(self,language):
        languageset=self.productlanguage_set.all()
        matches=[x for x in languageset if x.Language==language]
        if len(matches)==0:
            
            raise Exception('product {0} has no  language {1} version, its invalid,they are:{2}'.format(self.id,language,[str(x)+'|' for x in languageset]))
        elif len(matches)>1:
            raise Exception('product  has more than one ('+str(self.id)+') language versions, it is invalid')    
        else:
            return matches[0].Name
    def Snapshot(self):
        #self.productsnapshot_set.create  ProductSnapshot
        snapshot=self.productsnapshot_set.create(
            id=uuid.uuid4()
            #,theproduct=self
            ,CategoryCode=self.CategoryCode
            ,CreateTime=self.CreateTime
            ,LastUpdateTime=self.LastUpdateTime
            ,ModelNumber=self.ModelNumber
            ,SupplierCode=self.SupplierCode
            ,NTSCode=self.NTSCode
            ,OrderAmountMin=self.OrderAmountMin
            ,PriceOfFactory=self.PriceOfFactory
            ,ProductionCycle=self.ProductionCycle
            ,State=self.State
            ,TaxRate=self.TaxRate
            ,PriceDate=self.PriceDate
            ,PriceValidPeriod=self.PriceValidPeriod
            ,MoneyType=self.MoneyType
            ,ImageState=self.ImageState
            ,SyncState=self.SyncState
            ,SyncTime=self.SyncTime
            ,ProductCode=self.ProductCode
            ,ModelNumber_Original=self.ModelNumber
            )
        #self.productsnapshot_set.add(snapshot)
        for productlanguage in self.productlanguage_set.all():
            plsnap=snapshot.productlanguagesnapshot_set.create(
            Name=productlanguage.Name,PlaceOfDelivery=productlanguage.PlaceOfDelivery
            ,PlaceOfOrigin=productlanguage.PlaceOfOrigin
            ,ProductDescription=productlanguage.ProductDescription
            ,ProductParameters=productlanguage.ProductParameters
            ,Language=productlanguage.Language
            )
            #snapshot.productlanguagesnapshot_set.add(plsnap)
        #self.productsnapshot_set.add(snapshot)
        return snapshot
    def GetSnapshot(self,shottime):
        shotset=self.productsnapshot_set.all()
        print(list(shotset))
        return shotset.filter(ShotTime=min(enumerate(shotset),key=lambda x:x[0]-shottime))
    class Meta:
        db_table="product"
    def __str__(self):
        return self.GetName('en')#Productlanguage.LanguageChoices[0])
    
class ProductSnapshot(models.Model):
    '''keep a snapshot when it is modified
    '''
    id=UUIDField(primary_key=True)
    theproduct=ForeignKey(Product)
    ShotTime=DateTimeField("ShotTime",default=timezone.now())
    CategoryCode=CharField(max_length=255)
    CreateTime=DateTimeField('CreateTime',blank=True,null=True)
    LastUpdateTime=DateTimeField(blank=True,null=True)
    ModelNumber=CharField(max_length=255)
    SupplierCode=CharField(max_length=255)
    NTSCode=CharField(max_length=255)
    OrderAmountMin=DecimalField(max_digits=19,decimal_places=5,default=0)
    PriceOfFactory=CharField(max_length=255)
    ProductionCycle=DecimalField(max_digits=19,decimal_places=5,default=0)
    State=IntegerField(default=0)
    TaxRate=DecimalField(max_digits=19,decimal_places=5,default=0)
    PriceDate=CharField(max_length=255)
    PriceValidPeriod=CharField(max_length=255)
    MoneyType=CharField(max_length=255)
    ImageState=CharField(max_length=255)
    SyncState=IntegerField(default=0)
    SyncTime=DateTimeField(blank=True,null=True)
    ProductCode=CharField(max_length=255)
    ModelNumber_Original=CharField(max_length=255)
    def GetName(self,language):
        languageset=self.productlanguagesnapshot_set.all()
        matches=[x for x in languageset if x.Language==language]
        if len(matches)==0:
            raise Exception('productshot {0} has no  language {1} version, its invalid,they are:{2}'.format(self.id,language,[str(x)+'|' for x in languageset]))
        elif len(matches)>1:
            raise Exception('productshot  has more than one ('+str(self.id)+') language versions, it is invalid')    
        else:
            return matches[0].Name
    def __str__(self):
        return self.GetName('en') +' ShotTime:'+str(self.ShotTime)

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
    LanguageChoices=[('en','english'),('zh','chinese')]
    Language=CharField(max_length=2,choices=LanguageChoices,default='en')
    theproductsnapshot=ForeignKey(ProductSnapshot)
    def __str__(self):
        return 'Language:'+self.Language+' Name:'+self.Name
    
class ProductStock(models.Model):
    '''current stock quantity of a product
    
    '''
    Quantity=IntegerField()
    theproduct=ForeignKey(Product)
    def __str__(self):
        return str(self.theproduct)+':'+str(self.Quantity)
    #stock bill detail will change stock quantity or location
    

class StockLocation(models.Model):
    '''location infomation in the warehouse'''
    LocationCode=CharField(max_length=20)
    Name=CharField(max_length=20)
    Description=CharField(max_length=200)
    ParentLocation=ForeignKey('self',db_column='parentlocation',blank=True,null=True)
    stocks=ManyToManyField(ProductStock)
    def __str__(self):
        return self.LocationCode    
    def GetChildren(self):
        return self.stocklocation_set.all()#StockLocation.objects.filter(ParentLocation=self)
    
class BillBase(models.Model):
    '''base class of all bills 
    '''
    id=UUIDField(primary_key=True)#use uuid instead of autoincreament, to allow asigning an id to the object before saved into database
    BillNo=CharField(max_length=100,default=datetime.now().strftime('%Y%m%d%H%M%S'))
    BillTime=DateTimeField(auto_now_add=True)
    state_draft='draft' # saved for future change. not complete
    state_applied='applied'# appled for checking. can't change anymore 
    state_checked='checked'# ok
    State_Choices=((state_draft,'draft'),(state_applied,'applied'),
                    (state_checked,'checked'))
    BillState=CharField(max_length=10,choices=State_Choices,default=state_draft)
    Creator=ForeignKey(User)
    # staff-- not the login user who assonated with the bill
    StaffName=CharField(max_length=50,null=True,blank=True)
    Memo=CharField(max_length=1000,null=True,blank=True)
    
class StockBill(BillBase):
    '''bills record stock in and out'''
    BillType_Choices=(('in','stock in'),('out','stock out'))
    BillType=CharField(max_length=5, choices=BillType_Choices,default='in')
    Reason_Choices=(('in',
                         (
                          ('buy','buy'),
                          ('return','return back'),
                          ('inventory_profit','inventory profit'),
                          ('repaired','repaired'),
                          ('others','others')
                          )
                         ),
                        ('out',
                         (
                          ('sold','sold'),
                          ('borrowed','borrowed out'),
                          ('inventory_loss','inventory loss'),
                          ('damage','damage'),
                          ('others','others')
                          )
                         )
                        )
                         
    BillReason=CharField(max_length=20,choices=Reason_Choices,default='buy')
    TotalAmount=DecimalField(max_digits=10,decimal_places=2,default=0)
    # how many kinds of product in the bill
    TotalKinds=IntegerField(default=0)
    def __str__(self):
        return str(self.BillTime)+self.BillType
    def apply_stock_change(self):
        '''apply to stock,can;t changed anymore'''
        #self.BillState=BillBase.State_Choices.state_applied
        for detail in self.stockbilldetail_set.all():
            
            productstock,productstock_created=ProductStock.objects.get_or_create(theproduct__id=detail.product.id,
                                                            stocklocation__id=detail.location.id
                                                            ,defaults={'Quantity':(1 if self.BillType=='in' else -1)*detail.Quantity                                                          ,'theproduct':detail.product})
            if not productstock_created:
                productstock.Quantity+=(1 if self.BillType=='in' else -1)*detail.Quantity
            productstock.save()
            
    def save(self, *args, **kwargs):
        '''
            #just save to database , no effect to stock
        '''
        self.TotalAmount=sum(x.Quantity*Decimal(x.product.PriceOfFactory) for x in self.stockbilldetail_set.all())
        self.TotalKinds=len(self.stockbilldetail_set.all())
        logger.info('sdfasdf')
        super(StockBill,self).save(*args, **kwargs)
    def generat_detail_to_formatedtext(self):
        return [x.product.NTSCode+','+str(x.Quantity)+','+x.location.LocationCode
                            for x in self.stockbilldetail_set.all()]
class StockBillDetail(models.Model):
    '''product info in the bill'''
    stockbill=ForeignKey(BillBase,null=True)
    product=ForeignKey(Product)
    location=ForeignKey(StockLocation)
    Quantity=IntegerField()
    


    



    
    


    
    
