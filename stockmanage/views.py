from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.forms.formsets import formset_factory
from django.core import serializers
from stockmanage.models import Product,Productlanguage,StockLocation,StockBill
from stockmanage.forms import StockBillForm
# Create your views here.
def index(request):
    return render(request,'stockmanage/index.html')

##############Location COntrol#########################
def location_index(request):
    all_top_location=StockLocation.objects.filter(ParentLocation=None)
    return render(request,'stockmanage/stocklocation.html',{'all_top_locations':all_top_location})
    pass

def location_add_modify(request):
    location_id=request.POST.get('id')
    parentId =request.POST.get("parentId") 
    if parentId:
        parent=StockLocation.objects.get(pk=parentId)
    else:
        parent=None
    name = request.POST.get("name")
    code = request.POST.get("code")
    desc = request.POST.get("desc")
    location=StockLocation(Name=name,ParentLocation=parent,LocationCode=code,Description=desc)
    if location_id:
        location.id=int(location_id)
    location.save()
    return HttpResponse(location.id)
    
def location_get(request,location_id):
    location=StockLocation.objects.get(pk=location_id)
    jsonLocation=serializers.serialize('json', [location])

    return HttpResponse(jsonLocation,content_type="application/json")

def location_delete(request,location_id):
    location= StockLocation.objects.get(pk=location_id)
    location.delete()
    return HttpResponse("")

def stockbill_list(request):
    stockbill_list=StockBill.objects.all()
    return render(request,'stockmanage/stockbill.html',{'stockbill_list':stockbill_list})

def stockbill_in_index(request):
    return render(request,'stockmanage/stockbill.html')

def stockbill_out_index(request):
    return render(request,'stockmanage/stockbill.html')

def stockbill_create(request):
    return stockbill_edit(request,None)

def stockbill_edit(request,bill_id):
    form=StockBillForm()
    #import pdb; pdb.set_trace()
    if bill_id:
        bill=StockBill.objects.get(pk=bill_id)
    if request.method=="GET":
        form=StockBillForm(instance=bill)
    elif request.method=='POST':
        form=StockBillForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        return HttpResponse('Http method is invalid')
             
    return render(request,'stockmanage/stockbill_edit.html',{'form':form})
    pass

