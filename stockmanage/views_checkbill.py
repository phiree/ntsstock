import string

from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.core import serializers
from stockmanage.models import CheckBill,CheckBillDetail
from stockmanage.forms import StockBillForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.forms.models import inlineformset_factory
'''
stock check views
'''
def list(request):
    #import pdb;pdb.set_trace()
    p=request.POST
    if 'create' in p:
        create(request)
    return render(request,'stockmanage/checkbill.html',{'checkbill_list':CheckBill.objects.all()})
    pass
@require_http_methods(["POST"])
def create(request):
    #import pdb;pdb.set_trace()
    bill=CheckBill(Creator=request.user)
    bill.save()
    bill.CreateDetail()
    bill.save()
def edit(request,bill_id):
    bill=get_object_or_404(CheckBill,pk=bill_id)
    if request.method=="POST":
        p=request.POST
        if 'save' in p:
            detail_id_list=p.getlist('hi_detail_id')
            detail_realquantity_list=p.getlist('tbx_realquantity')
            for counter,detail_id in enumerate(detail_id_list):
                detail=CheckBillDetail.objects.get(pk=detail_id)
                detail.realquantity=int(detail_realquantity_list[counter])
                detail.save()          
            pass
        elif 'begin_check':
            bill.CheckState='progressing' 
            bill.save()
            pass
        elif 'download_as_excel':
            pass
        elif 'complete_check':
            '''
            保存输入结果,生成盘盈盘亏单.
            '''
            pass
        else:
            pass
    return render(request,'stockmanage/checkbill_edit.html',{'bill':bill})
    pass

