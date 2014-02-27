import string
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.core import serializers
from stockmanage.models import Product,Productlanguage,StockLocation,StockBill,StockBillDetail,ProductStock
from stockmanage.forms import StockBillForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
# Create your views here.

def list(request):
    return render(request,'stockmanage/productstock.html',{'productstock_list':ProductStock.objects.all()})
    pass
