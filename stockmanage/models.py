import uuid, time, logging
from django.contrib.auth.models import User

from datetime import datetime
from decimal import Decimal
from django.utils import timezone
from django.db import models
from django_extensions.db.fields import UUIDField
from django.db.models.fields import CharField, DecimalField, IntegerField, DateTimeField, TextField, \
    Field
from django.db.models.fields.related import ForeignKey, ManyToManyField
from model_utils.managers import InheritanceManager
logger = logging.getLogger(__name__)


class Product(models.Model):
    id = UUIDField(primary_key=True)
    SerialNo = IntegerField(default=0, null=True)
    Code_Original = CharField(max_length=50)
    Code_Database = CharField(max_length=50)
    NTSCode = CharField(max_length=255)
    Name = CharField(max_length=255)
    ModelNumber = CharField(max_length=255)
    Specification = CharField(max_length=1000)
    Material = CharField(max_length=255)
    Price = DecimalField(max_digits=10, decimal_places=2)
    Currency = CharField(max_length=10, default='CNY')
    Unit = CharField(max_length=10)
    CreateTime = DateTimeField('CreateTime', blank=True, default=datetime.now())
    LastUpdateTime = DateTimeField(blank=True, default=datetime.now())
    SupplierCode = CharField(max_length=255)
    State = IntegerField(default=0)

    def Snapshot(self):
        # self.productsnapshot_set.create  ProductSnapshot
        snapshot = self.productsnapshot_set.create(
            id=uuid.uuid4()
            # ,product=self
            , SerialNo=self.SerialNo
            , Code_Original=self.Code_Original
            , Code_Database=self.Code_Database
            , Name=self.Name
            , Unit=self.Unit
            , CreateTime=self.CreateTime
            , LastUpdateTime=self.LastUpdateTime
            , ModelNumber=self.ModelNumber
            , SupplierCode=self.SupplierCode
            , Specification=self.Specification
            , Material=self.Material
            , Price=self.Price
            , Currency=self.Currency
            , State=self.State

        )
        return snapshot

    def GetSnapshot(self, shottime):
        shotset = self.productsnapshot_set.all()
        print(list(shotset))
        return shotset.filter(ShotTime=min(enumerate(shotset), key=lambda x: x[0] - shottime))

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.Name


class ProductSnapshot(models.Model):
    '''keep a snapshot when it is modified
    '''
    product = ForeignKey(Product)
    ShotTime = DateTimeField("ShotTime", default=timezone.now())

    id = UUIDField(primary_key=True)
    SerialNo = IntegerField(default=0)
    Code_Original = CharField(max_length=50)
    Code_Database = CharField(max_length=50)
    Name = CharField(max_length=255)
    ModelNumber = CharField(max_length=255)
    Specification = CharField(max_length=1000)
    Material = CharField(max_length=255)
    Price = DecimalField(max_digits=10, decimal_places=2)
    Currency = CharField(max_length=10, default='CNY')
    Unit = CharField(max_length=10)
    CreateTime = DateTimeField('CreateTime', blank=True, default=datetime.now())
    LastUpdateTime = DateTimeField(blank=True, default=datetime.now())
    SupplierCode = CharField(max_length=255)
    State = IntegerField(default=0)


class StockLocation(models.Model):
    '''location infomation in the warehouse'''
    LocationCode = CharField(max_length=20)
    Name = CharField(max_length=20)
    Description = CharField(max_length=200)
    ParentLocation = ForeignKey('self', db_column='parentlocation', blank=True, null=True)
    # stocks=ManyToManyField(ProductStock)
    def __str__(self):
        return self.LocationCode

    def GetChildren(self):
        return self.stocklocation_set.all()  # StockLocation.objects.filter(ParentLocation=self)


class ProductStock(models.Model):
    '''current stock quantity of a product
    
    '''
    quantity = IntegerField()
    product = ForeignKey(Product)
    stocklocation = ForeignKey(StockLocation, null=True)
    memo = CharField(max_length=2000)
    last_check_time = DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.product.id) + ':' + str(self.quantity) + ':' + str(self.stocklocation)
        # stock bill detail will change stock quantity or location

class BillBase(models.Model):
    '''base class of all bills (stock_in_bill,stock_out_bill)
    '''
    objects=InheritanceManager()
    id = UUIDField(
        primary_key=True)  # use uuid instead of autoincreament, to allow asigning an id to the object before saved into database
    BillNo = CharField(max_length=100, default=datetime.now().strftime('%Y%m%d%H%M%S'), editable=False)
    BillTime = DateTimeField(auto_now_add=True)
    state_draft = 'draft'  # saved for future change. not complete
    state_applied = 'applied'  # appled for checking. can't change anymore 
    state_checked = 'checked'  # ok
    State_Choices = ((state_draft, 'draft'), (state_applied, 'applied'),
                     (state_checked, 'checked'))
    BillState = CharField(max_length=10, choices=State_Choices, default=state_draft)

    Creator = ForeignKey(User)
    # staff-- not the login user who assonated with the bill
    StaffName = CharField(max_length=50, null=True, blank=True)
    Memo = CharField(max_length=1000, null=True, blank=True)
    RelatedBill=ForeignKey('self',null=True)
    def generat_detail_to_formatedtext(self):
        return [x.product.Code_Original
                for x in self.billdetailbase_set.all()]
    def parse_detail_from_formated_text(self,formated_text):
        detail_list=[]
        for line in formated_text.splitlines():
            if not line:
                continue
            detail=self.parse(line)
            detail_list.extend(detail)
        self.billdetailbase_set.add(*detail_list)
        #return detail_list

    def parse(self,line):
        pass
    def generat_detail_to_formatedtext(self):
        pass

class StockBill(BillBase):
    '''bills record stock in and out'''
    BillType_Choices = (('in', 'stock in'), ('out', 'stock out'))
    BillType = CharField(max_length=5, choices=BillType_Choices, default='in')
    #BillNo= CharField(max_length=100, default=datetime.now().strftime('%Y%m%d%H%M%S'))

    Reason_Choices = (('in',
                       (
                           ('buy', 'buy'),
                           ('return', 'return back'),
                           ('inventory_profit', 'inventory profit'),
                           ('repaired', 'repaired'),
                           ('others', 'others')
                       )
                      ),
                      ('out',
                       (
                           ('sold', 'sold'),
                           ('borrowed', 'borrowed out'),
                           ('inventory_loss', 'inventory loss'),
                           ('damage', 'damage'),
                           ('others', 'others')
                       )
                      )
    )


    # how many kinds of product in the bill
    def get_totalamount(self):
        return sum(x.quantity * Decimal(x.product.Price) for x in self.billdetailbase_set.all())
    def get_totalkind(self):
        return len(self.billdetailbase_set.all())
    BillReason = CharField(max_length=20, choices=Reason_Choices)
    TotalAmount = property(get_totalamount)
    TotalKinds = property(get_totalkind)

    def __str__(self):
        return str(self.BillTime) + self.BillType

    def apply_stock_change(self):
        '''apply to stock,can;t changed anymore'''
        # self.BillState=BillBase.State_Choices.state_applied

        for detail in self.billdetailbase_set.all():

            productstock, productstock_created = ProductStock.objects.get_or_create( product__id=detail.product.id,
                                                                                    stocklocation__id=detail.location.id
                                                                                    , defaults={
                    'Quantity': (1 if self.BillType == 'in' else -1) * detail.quantity,
                    'product': detail.product,
                    'stocklocation': detail.location})
            print(productstock_created)
            if not productstock_created:
                productstock.quantity += (1 if self.BillType == 'in' else -1) * detail.quantity
                # else:
                # productstock.stocklocation_set.add(detail.location)
                # detail.location.stocks.add(productstock)
                # detail.location.save()
            productstock.save()

    def save(self, *args, **kwargs):
        #import pdb;pdb.set_trace()
        if not self.id:
            self.BillNo = self.BillType.upper() + self.BillNo
        if self.BillState == StockBill.state_applied:
            print('beigin_apply_stock_change')
            self.apply_stock_change()

        logger.info('sdfasdf')
        super(StockBill, self).save(*args, **kwargs)

    def generat_detail_to_formatedtext(self):
        return [x.product.Code_Original + ',' + str(x.quantity) + ',' + x.location.LocationCode
                for x in self.billdetailbase_set.all().select_subclasses()]

    def parse(self,line):
        procode=line.split(',')[0]
        product=Product.objects.get(Code_Original=procode)
        qty=line.split(',')[1]
        location_code=line.split(',')[2]
        location=StockLocation.objects.get(LocationCode=location_code)
        detail=StockBillDetail(stockbill=bill,product=product,location=location,quantity=qty)
        return detail

class BillDetailBase(models.Model):
    billbase = ForeignKey(BillBase, null=True)
    product = ForeignKey(Product)
    quantity = IntegerField()
    objects=InheritanceManager()

class StockBillDetail(BillDetailBase):
    '''product info in the bill'''
    location = ForeignKey(StockLocation,null=True)

class StockTransDetail(BillDetailBase):
    location_from=ForeignKey(StockLocation,null=True,related_name='location_from')
    location_to=ForeignKey(StockLocation,null=True, related_name='location_to')

class StockTransBill(BillBase):
    pass
class CheckBill(BillBase):
    CheckTime_Begin = DateTimeField(blank=True, default=datetime.now())
    CheckTime_Complete = DateTimeField(null=True)

    CheckState_Choices = (('darft', 'not begin'), ('progressing', 'began check'), ('complete', 'complete checking'))
    CheckState = CharField(max_length=20, choices=CheckState_Choices, default='draft')

    def Check(self):
        pass

    def CreateDetail(self, condition):
        '''
           Create check detail, save into database;
       '''
        check_list = self.GenerateDetail(condition)
        for ps in check_list:
            cbdetail = CheckBillDetail(product=ps. product,
                                       location=ps.stocklocation,
                                       realquantity=ps.quantity,
                                       quantity=ps.quantity)
            self.checkbilldetail_set.add(cbdetail)

    def GenerateDetail(self, condition):
        '''
        generate Candidated details , for choosen 
        '''
        check_list = []
        if not condition:
            check_list = ProductStock.objects.all()
        else:
            if condition.type == 'location':
                location_list = condition.location_list
                check_list = ProductStock.objects.filter(stocklocation__LocationCode__in=location_list)
            elif condition.type == 'random':
                amount = condition.amount
                for i in range(1, amount):
                    check_list.add(CheckBillDetail().get_random())
            elif condition.type == 'defined_list':
                check_list = ProductStock.objects.filter( product__Code_Original__in=condition.defined_list)
            else:
                raise Exception('No Such Type')
        return check_list

    def GenerateChangeDetail(self):
        '''结束盘点 生成 盘盈 盘亏数据'''
        list_change=[]
        #import pdb;pdb.set_trace()
        for detail in CheckBillDetail.objects.filter(billbase__id=self.id):

            generated_detail=detail.GenerateStockDetail()
            if generated_detail:
                list_change.append(generated_detail)
        return list_change
    def parse(self,line):
        '''override super methoed'''
        procode=line
        # one product maybe in different locations
        #product=Product.objects.get(Code_Original=procode)
        productstock_list=ProductStock.objects.filter(product__Code_Original=procode)
        checkdetail_list=[]
        for productstock in productstock_list:
            #import pdb;pdb.set_trace()
            #basebilldetail= StockBillDetail(stockbill=self,product=productstock.product,location=productstock.stocklocation,quantity=productstock.quantity)
            checkbilldetail=CheckBillDetail(billbase=self,product=productstock. product,location=productstock.stocklocation,quantity=productstock.quantity,realquantity=None)
            checkdetail_list.append(checkbilldetail)
        return checkdetail_list
    def IsProgressing(self):
        pass
    def generat_detail_to_formatedtext(self):
        return [x.product.Code_Original
                for x in self.billdetailbase_set.all()]


class CheckBillDetail(StockBillDetail):
    realquantity = IntegerField(null=True)
    def get_random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]

    def GenerateStockDetail(self):

        change = self.realquantity - self.quantity
        if change == 0:
            return None
        stockdetail = StockBillDetail( product=self.product, location=self.location, quantity=change)
        return stockdetail




class Suppier(models.Model):
    pass    


    
    


    
    
