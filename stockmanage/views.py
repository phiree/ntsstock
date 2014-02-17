from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from stockmanage.models import Product,Productlanguage,StockLocation,StockBill
# Create your views here.
def index(request):
    return render(request,'stockmanage/index.html')

##############Location COntrol#########################
def location_index(request):
    all_top_location=StockLocation.objects.filter(ParentLocation=None)
    return render(request,'stockmanage/stocklocation.html',{'all_top_locations':all_top_location})
    pass

def location_manage(request):
    t=request.POST.get('actiontype')
    location_id=int(request.POST.get('id') or 0)
    
    print(location_id)
    if t=='position_addmodify':
    #增加或者修改
        parentId =int(request.POST.get("parentId") or 0)
        if parentId:
            parent=StockLocation.objects.filter(ParentLocation__id=parentId)[0]
        else:
            parent=None
        name = request.POST.get("name")
        code = request.POST.get("code")
        desc = request.POST.get("desc")
        location=StockLocation(Name=name,ParentLocation=parent,LocationCode=code,Description=desc)
        if location_id:
            location.id=location_id
        location.save()
    elif t=='position_get':
        location=StockLocation.objects.get(pk=location_id)
    return HttpResponse(location.id)