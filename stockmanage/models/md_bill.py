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
            # ,theproduct=self
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
    theproduct = ForeignKey(Product)
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
    theproduct = ForeignKey(Product)
    stocklocation = ForeignKey(StockLocation, null=True)
    memo = CharField(max_length=2000)
    last_check_time = DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.theproduct.id) + ':' + str(self.Quantity) + ':' + str(self.stocklocation)
        # stock bill detail will change stock quantity or location

class BillBase(models.Model):
    '''base class of all bills (stock_in_bill,stock_out_bill)
    '''
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
    def generat_detail_to_formatedtext(self):
        return [x.product.Code_Original
                for x in self.stockbilldetail_set.all()]


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
        return sum(x.quantity * Decimal(x.product.Price) for x in self.stockbilldetail_set.all())

    def get_totalkind(self):
        return len(self.stockbilldetail_set.all())

    BillReason = CharField(max_length=20, choices=Reason_Choices)

    TotalAmount = property(get_totalamount)
    TotalKinds = property(get_totalkind)

    def __str__(self):
        return str(self.BillTime) + self.BillType

    def apply_stock_change(self):
        '''apply to stock,can;t changed anymore'''
        # self.BillState=BillBase.State_Choices.state_applied

        for detail in self.stockbilldetail_set.all():

            productstock, productstock_created = ProductStock.objects.get_or_create(theproduct__id=detail.product.id,
                                                                                    stocklocation__id=detail.location.id
                                                                                    , defaults={
                    'Quantity': (1 if self.BillType == 'in' else -1) * detail.Quantity,
                    'theproduct': detail.product,
                    'stocklocation': detail.location})
            print(productstock_created)
            if not productstock_created:
                productstock.Quantity += (1 if self.BillType == 'in' else -1) * detail.Quantity
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
        return [x.product.Code_Original + ',' + str(x.Quantity) + ',' + x.location.LocationCode
                for x in self.stockbilldetail_set.all()]


class StockBillDetail(models.Model):
    '''product info in the bill'''
    stockbill = ForeignKey(StockBill, null=True)
    product = ForeignKey(Product)
    location = ForeignKey(StockLocation)
    Quantity = IntegerField()


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
            cbdetail = CheckBillDetail(product=ps.theproduct,
                                       location=ps.stocklocation,
                                       realquantity=ps.Quantity,
                                       quantity=ps.Quantity)
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
                check_list = ProductStock.objects.filter(theproduct__Code_Original__in=condition.defined_list)
            else:
                raise Exception('No Such Type')
        return check_list

    def CompleteCheck(self):
        '''结束盘点 生成盘盈盘亏单据'''

        check_stockin_bill = StockBill(BillType='in', BillState='applied',
                                       StaffName=self.StaffName, Creator=self.Creator,
                                       BillReason='inventory_profit')
        check_stockout_bill = StockBill(BillType='out', BillState='applied',
                                        StaffName=self.StaffName, Creator=self.Creator,
                                        BillReason='inventory_loss')
        #check_stockout_bill.save()
        #check_stockin_bill.save()
        #import pdb;pdb.set_trace()
        for detail in self.checkbilldetail_set.all():
            detail.GenerateStockDetail(check_stockout_bill, check_stockin_bill)
        if len(check_stockout_bill.stockbilldetail_set.all()) > 0:
            #check_stockout_bill.save()
            pass
        if len(check_stockin_bill.stockbilldetail_set.all()) > 0:
            #check_stockin_bill.save()
            pass

    def IsProgressing(self):
        pass


class CheckBillDetail(StockBillDetail):
    realquantity = IntegerField()

    def get_random(self):
        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]

    def GenerateStockDetail(self, stockout, stockin):
        '''if realquantity is not equal to systemquantity
            create a stockdetail'''
        change = self.realquantity - self.Quantity
        change_abs = abs(change)
        if change == 0:
            return None
        stockdetail = StockBillDetail(product=self.product, location=self.location, Quantity=change_abs)
        stockdetail.stockbill = stockin if change > 0 else stockout
        if change > 0:
            stockin.stockbilldetail_set.add(stockdetail)
        else:
            stockout.stockbilldetail_set.add(stockdetail)


class CheckBillRealDetail(models.Model):
    pass


class Suppier(models.Model):
    pass    


    
    


    
    
