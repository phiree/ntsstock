import string
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.core import serializers
from stockmanage.models import Product,StockLocation,StockBill,StockBillDetail,ProductStock,BillBase,BillDetailBase
from stockmanage.forms import StockBillForm
#from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from stockmanage.paging_extra import ExPaginator
from stockmanage.tables3 import table2_productstock
from django.views.generic import ListView
#from paging_extra import ExPaginator
#import simple_paginator
# Create your views here.
class ProductStockList(ListView):
    model=ProductStock
    paginate_by=2
    context_object_name ='productstock_list_page'
    def get_queryset(self):
        #import pdb;pdb.set_trace()
        kw=self.request.GET.get('kw')
        productstock_list=[]

        if not kw:
            productstock_list=ProductStock.objects.all()
        else:
            productstock_list=ProductStock.objects.filter(Q( product__Name__contains=kw )|\
                                                       Q( product__Code_Original__contains=kw))
        return productstock_list
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductStockList, self).get_context_data(**kwargs)
        # Add in the publisher
        context['kw'] = self.request.GET.get('kw') if self.request.GET.get('kw') else ''
        return context

def list(request):
    
    return list_search(request)
def list_search(request):
    
    kw=request.GET.get('kw')
    productstock_list=[]
    
    if not kw:
        productstock_list=ProductStock.objects.all()
    else:
        productstock_list=ProductStock.objects.filter(Q( product__Name__contains=kw )|\
                                                       Q( product__Code_Original__contains=kw))
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
    
    table=table2_productstock(productstock_list)
    table.paginate(page=request.GET.get('page', 1), per_page=25)
    return render(request,'stockmanage/productstock_list.html',{'productstock_list_page':productstock_list_page,
                                                           'productstock_list':productstock_list,
                                                           'table':table,
                                                           'paginator':paginator,
                                                           'range':paginator.page_range,
                                                            'kw':kw if kw else ''}
                 )
class StockTraceList(ListView):
    model=BillBase
    paginate_by=20
    context_object_name ='trace_list'
    def get_queryset(self):
        #import pdb;pdb.set_trace()
        product_id=self.kwargs.get('product_id')
        trace_list=StockBill.objects.filter(billdetailbase__product__id=product_id).order_by('BillTime')
        for trace in trace_list:
            quantity=trace.billdetailbase_set.all()[0].quantity
            trace.quantity=quantity
        return trace_list
def stock_trace_list(request,product_id):
    '''trace of stock change of a product'''
    #import pdb;pdb.set_trace()
    trace_list=BillBase.objects.filter(billdetailbase__product__id=product_id).select_subclasses()
    return render(request,'stockmanage/stocktrace_list.html',
                  {'trace_list':trace_list})

def productstock_search(keyword):
    
    pass
    
