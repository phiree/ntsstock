import string
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.core import serializers
from stockmanage.models import Product,Productlanguage,StockLocation,StockBill,StockBillDetail
from stockmanage.forms import StockBillForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

def index(request):
    #import pdb;pdb.set_trace()
   
    return render(request,'stockmanage/index.html')
def logout(request):
    logout(request)
    HttpResponseRedirect('/')
##############Location COntrol#########################

def location_index(request):
    if not request.user.is_authenticated():
        return redirect('/login/?next=%s' % request.path)
    #import pdb;pdb.set_trace()
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

def stockbill_list(request,type):
    stockbill_list=StockBill.objects.filter(BillType=type).order_by('-BillTime')
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

    return render(request,'stockmanage/stockbill.html',
                  {'stockbill_list':stockbill_list_page,'paginator':paginator,
                   'page':stockbill_list_page,
                   'range':paginator.page_range})

def stockbill_stockin_list(request):
    return stockbill_list(request,'in')
    
def stockbill_stockout_list(request):
    return stockbill_list(request,'out')
    
def stockbill_stockout_create(request):
    action='create'
    return stockbill_edit(request,'out',None,action)

def stockbill_stockin_create(request):
    action='create'
    #import pdb; pdb.set_trace()
    return stockbill_edit(request,'in',None,action)

def stockbill_stockin_edit(request,bill_id):
    return stockbill_edit(request,'in',bill_id,'.')

def stockbill_stockout_edit(request,bill_id):
    return stockbill_edit(request,'out',bill_id,'.')

def stockbill_edit(request,type,bill_id,action):
    #import pdb; pdb.set_trace()
    if bill_id:
        bill=StockBill.objects.get(pk=bill_id)
    else:
        bill=StockBill(BillType=type,Creator=request.user)
        bill.BillNo=bill.BillType.upper()+bill.BillNo
    detaillist_formated_text= bill.generat_detail_to_formatedtext()
    if request.method=="GET":
        billform=StockBillForm(instance=bill)
        #import pdb;pdb.set_trace()
        return render(request,'stockmanage/stockbill_edit.html',
                      {'form':billform,
                     #'inline_detain_formset':detail_inlineformset,
                     'detaillist_formated_text':'\n'.join(detaillist_formated_text),
                     'bill':bill,'action':action})
 
    elif request.method=='POST':
        #import pdb;pdb.set_trace()
        p=request.POST.copy()
        if 'savedraft' in p:
            pass
        elif 'apply' in p:
            bill.BillState='applied'
            #bill.apply_stock_change()
            pass
        elif 'pass' in p:
            p["BillReason"]=bill.BillReason
            bill.BillState='checked'
        elif 'refused' in p:
            p["BillReason"]=bill.BillReason
            bill.BillState='draft'
        elif 'tt_billdetail' in p:
           return stockbill_update_detail(request,bill)
        else:
            raise Exception('No Such Action')
        #import pdb; pdb.set_trace()
        
        #form=StockBillForm(request.POST,instance=bill)
        billform=StockBillForm(p,instance=bill)
        #detail_inlineformset=billdetail_formset_factory(request.POST,request.FILES, instance=bill)
        if billform.is_valid():
            billform.save()
        
            
            #if detail_inlineformset.is_valid():
                #detail_inlineformset.save()
        if not bill_id:
            return HttpResponseRedirect(reverse('stockmanage:stockbill_stockin_edit',args=[bill.id]))
       
    return render(request,'stockmanage/stockbill_edit.html',
              {'form':billform,
             'detaillist_formated_text':'\n'.join(detaillist_formated_text),
             'bill':bill,'action':action})     
    
def stockbill_update_detail(request,bill):
    
    detaillist=bill.stockbilldetail_set.all()
    bill.stockbilldetail_set.clear()
    detaillist=[]
    formated_text=request.POST['tt_billdetail']
    for line in formated_text.splitlines():
        if not line:
            continue
        #import pdb;pdb.set_trace()
        procode=line.split(',')[0]
        product=Product.objects.get(NTSCode=procode)
        qty=line.split(',')[1]
        location_code=line.split(',')[2]
        location=StockLocation.objects.get(LocationCode=location_code)
        detail=StockBillDetail(stockbill=bill,product=product,location=location,Quantity=qty)
        #[bill.stockbilldetail_set].append(detail) # 
        bill.stockbilldetail_set.add(detail)
        detaillist_formated_text=bill.generat_detail_to_formatedtext()
    return render(request,'stockmanage/stockbill_edit.html',
                      {'form':StockBillForm(instance=bill),
                     #'inline_detain_formset':detail_inlineformset,
                     'detaillist_formated_text':'\n'.join(detaillist_formated_text),
                     'bill':bill,'action':'.'})
def productstock_list(request):
    return HttpResponse('产品库存列表')
    pass
