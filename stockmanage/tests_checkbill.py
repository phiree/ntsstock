from django.test import TestCase
from random import choice
from django.utils import timezone
import datetime
from django.contrib.auth.models import User
from autofixture import  AutoFixture,generators
from stockmanage.models import  Product,StockLocation,ProductStock,ProductSnapshot,StockBill,StockBillDetail,CheckBill,CheckBillDetail
# Create your tests here.
class test_checkbill(TestCase):
    def test_GenerateChangeDetail(self):
        af_checkbill=AutoFixture(CheckBill,generate_fk=True)
        bill=af_checkbill.create(1)[0]

        af_checkbilldetail=AutoFixture(CheckBillDetail, generate_fk=True,field_values={'stockbill':bill,'quantity':1,'realquantity':4})
        billdetails=af_checkbilldetail.create(4)
        self.assertEqual(4,len(billdetails))
        change_list=bill.GenerateChangeDetail()
        self.assertEqual(4,len(change_list))
        for change in change_list:
            self.assertEqual(change.quantity,3)