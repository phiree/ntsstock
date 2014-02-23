import string
from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.forms.formsets import formset_factory
from django.core import serializers
from stockmanage.models import Product,Productlanguage,StockLocation,StockBill,StockBillDetail
from stockmanage.forms import StockBillForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
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
    stockbill_list=StockBill.objects.all().order_by('-BillTime')
    paginator = Paginator(stockbill_list, 5) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        stockbill_list_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        stockbill_list_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        stockbill_list_page = paginator.page(paginator.num_pages)

    return render(request,'stockmanage/stockbill.html',{'stockbill_list':stockbill_list_page,'paginator':paginator})

def stockbill_in_index(request):
    return render(request,'stockmanage/stockbill.html')

def stockbill_out_index(request):
    return render(request,'stockmanage/stockbill.html')

def stockbill_create(request):
    return stockbill_edit(request,None)

def stockbill_edit(request,bill_id):
    #import pdb; pdb.set_trace()
    if bill_id:
        bill=StockBill.objects.get(pk=bill_id)
        if not bill.BillState ==StockBill.state_draft:
            
            pass
    else:
        bill=StockBill()
            # can't modify any more
    if request.method=="GET":
        form=StockBillForm(instance=bill)
    elif request.method=='POST':
        #import pdb; pdb.set_trace()
        bill.BillState=request.POST.get('BillState')
        
        form=StockBillForm(request.POST,instance=bill)
        if form.is_valid():
            form.save()
    else:
        return HttpResponse('Http method is invalid')
             
    return render(request,'stockmanage/stockbill_edit.html',{'form':form})
    pass
def stockbill_update_detail(request,bill_id):
    bill=StockBill.objects.get(pk=bill_id)
    detaillist=bill.stockbilldetail_set.all()
    if request.method=="GET":
        
        detaillist=StockBill.objects.get(pk=bill_id).stockbilldetail_set.all()
        formated_text='\n'.join([x.product.NTSCode+','+x.location.LocationCode+','+str(x.Quantity)
                            for x in detaillist])
    else:
        bill.stockbilldetail_set.clear()
        detaillist=[]
        formated_text=request.POST['tt_billdetail']
        for line in formated_text.splitlines():
            if not line:
                continue
            procode=line.split(',')[0]
            product=Product.objects.get(NTSCode=procode)
            qty=line.split(',')[1]
            location_code=line.split(',')[2]
            location=StockLocation.objects.get(LocationCode=location_code)
            detail=StockBillDetail(stockbill=bill,product=product,location=location,Quantity=qty)
            #[bill.stockbilldetail_set].append(detail) # 
            bill.stockbilldetail_set.add(detail)
            #import pdb;pdb.set_trace()
        #import pdb;pdb.set_trace()
        bill.save()
    return render(request,'stockmanage/stockbilldetail_list.html',{'bill':bill,'formated_text':formated_text})
        
       
    
