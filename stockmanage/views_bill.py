import datetime
import string
from django.middleware import transaction

from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.core import serializers
from django.db import IntegrityError
from stockmanage.models import CheckBill,CheckBillDetail,BillBase,StockBill
from stockmanage.forms import StockBillForm,CheckBillGenerateForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.forms.models import inlineformset_factory
from django.views.generic import ListView
'''
bill list views
'''
class BillListView(ListView):
    model=BillBase
    paginate_by=20
    def get_queryset(self):
        #import pdb;pdb.set_trace()
        #determine bill type
        billtype=self.kwargs.get('billtype')
        print(billtype)
        if billtype.lower()=='checkbill':
            bill_list=CheckBill.objects.order_by('BillTime')
        elif billtype.lower()=='stockbill':
            bill_list=StockBill.objects.order_by('BillTime')
        elif billtype.lower()=='stocktransbill':
            bill_list=StockTransBill.objects.order_by('BillTime')
        else:
            bill_list=[]
        return bill_list

