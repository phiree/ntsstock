from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.core import serializers
from stockmanage.models import Product,Productlanguage,StockLocation,StockBill
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


