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
from stockmanage.models import CheckBill,CheckBillDetail
from stockmanage.forms import StockBillForm,CheckBillGenerateForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.forms.models import inlineformset_factory

'''
stock check views
'''
def list(request):
    #import pdb;pdb.set_trace()
    p=request.POST
    if 'create' in p:
        bill=create(request)
        return HttpResponseRedirect(reverse('stockmanage:checkbill_edit',args=(bill.id,)))
    checkbill_list=CheckBill.objects.all()
    
    
    paginator = Paginator(checkbill_list, 10)
    count=CheckBill.objects.count()
    paginator._count=count
    page = request.GET.get('page')
    try:
        checkbill_list_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        checkbill_list_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        checkbill_list_page = paginator.page(paginator.num_pages)
    return render(request,'stockmanage/checkbill.html',{'checkbill_list':checkbill_list_page,
                                                        'paginator':paginator,'range':paginator.page_range,
                                                        'page':checkbill_list_page})
    pass

def create(request):
    if request.method=='POST':
        #import pdb;pdb.set_trace()
        bill=CheckBill(Creator=request.user)
        bill.save()
        generate_type=request.POST.get('type')
        generate_condition={}
        generate_condition.type=generate_type
        #location,random,defined_list
        if generate_type=='random':
            generate_amount=request.GET.get('generate_amount')
            generate_amount=int(generate_amount)
        bill.CreateDetail()
        bill.save()
        return bill
    elif request.method=='GET':
        generate_form=CheckBillGenerateForm()
        return render(request,'stockmanage/checkbill_create_edit.html',{'generate_form':generate_form,})
    else:
        raise Exception('Error Method')
        
def input_realquantity(request,bill_id):
    #import pdb;pdb.set_trace()
    bill=get_object_or_404(CheckBill,pk=bill_id)
    if request.method=="POST":
        p=request.POST
        
        if 'begin_check' in p:
            bill.CheckState='progressing' 
            bill.save()
            pass
        elif 'download_as_excel' in p:
            #import pdb;pdb.set_trace()
            from stockmanage.excel_handler import excel_writer
            ew=excel_writer(bill.checkbilldetail_set.all(),['product','location','quantity'],bill.BillNo)
            
            wb=ew.write()
            
            response = HttpResponse(mimetype="application/ms-excel")
            response['Content-Disposition'] = 'attachment; filename=%s' %  bill.BillNo+'.xls'
            wb.save(response)
            return response
        
        elif 'complete_check' in p or 'save' in p:
            '''
            保存输入结果,生成盘盈盘亏单.
            '''
            detail_id_list=p.getlist('hi_detail_id')
            detail_realquantity_list=p.getlist('tbx_realquantity')
            for counter,detail_id in enumerate(detail_id_list):
                detail=CheckBillDetail.objects.get(pk=detail_id)
                detail.realquantity=int(detail_realquantity_list[counter])
                detail.save()
            if 'complete_check' in p:
                bill.CheckState='complete'
                bill.CheckTime_Complete=datetime.now()
                bill.save()
                try:
                    bill.CompleteCheck()
                except IntegrityError:
                    transaction.rollback()
                except:
                    raise
            
        else:
            pass
    return render(request,'stockmanage/checkbill_input_realquantity.html',{'bill':bill})
    pass

