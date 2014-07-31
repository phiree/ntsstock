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
from django.views.generic.detail import DetailView
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
        if not billtype:
            bill_list=BillBase.objects.all().select_subclasses()
        else:
            #real_cls=eval(billtype)
            real_cls=globals()[billtype]
            return real_cls.objects.all()
        return bill_list

class BillDetailView(DetailView):
    model=BillBase


