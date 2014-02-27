import string
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.core import serializers
from stockmanage.models import CheckBill,CheckBillDetail
from stockmanage.forms import StockBillForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
'''
stock check views
'''
def list(request):
    return render(request,'stockmanage/checkbill.html',{'checkbill_list':CheckBill.objects.all()})
    pass
def create(request):
    bill=CheckBill()
    bill.save()
    bill.CreateDetail()
    bill.save()
    return render(request,'stockmanage/checkbill.html',{'checkbill_list':CheckBill.objects.all()})
def edit(request):
    pass

