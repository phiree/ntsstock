import string
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.core import serializers
from stockmanage.models import Product,StockLocation,StockBill,StockBillDetail,ProductStock
from stockmanage.forms import StockBillForm
#from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from stockmanage.paging_extra import ExPaginator
#from paging_extra import ExPaginator
#import simple_paginator
# Create your views here.
def list(request):
    
    return list_search(request)
def list_search(request):
    
    kw=request.GET.get('kw')
    productstock_list=[]
    
    if not kw:
        productstock_list=ProductStock.objects.all()
    else:
        productstock_list=ProductStock.objects.filter(theproduct__Name__contains=kw)
        #productstock_list
    paginator = ExPaginator(productstock_list, 50) # Show 25 contacts per page
    page = request.GET.get('page')
    productstock_list_page = paginator.page(page)
    #objects=productstock_list
    #paginator._count=100
    '''try:
        productstock_list_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        productstock_list_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        productstock_list_page = paginator.page(paginator.num_pages)
        '''
    return render(request,'stockmanage/productstock.html',{'productstock_list_page':productstock_list_page,
                                                           'productstock_list':productstock_list,
                                                           'paginator':paginator,
                                                           'range':paginator.page_range,
                                                            'kw':kw if kw else ''}
                 )
    pass

def stock_trace_list(request,product_id):
    '''trace of stock change of a product'''
    #import pdb;pdb.set_trace()
    detail_list=StockBillDetail.objects.filter(product__id=product_id,stockbill__BillState='applied')
    return render(request,'stockmanage/stocktrace.html',
                  {'trace_list':detail_list})

def productstock_search(keyword):
    
    pass
    
