import string
from datetime import datetime
from django.forms.models import inlineformset_factory
from django.utils import timezone
from django.shortcuts import render,get_object_or_404,render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import  reverse
from django.views import generic
from django.core import serializers
from stockmanage.models import Product,StockLocation,StockBill,StockBillDetail,CheckBill,CheckBillDetail
from stockmanage.forms import StockBillForm,CheckBillGenerateForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import View,ListView
from model_utils.managers import InheritanceManager
'''
stock check views
'''
class CheckBillList(ListView):
    model=CheckBill
    paginate_by=2

def create(request):
    return edit(request)
def edit(request,bill_id=None):
    if bill_id:
        checkbill=CheckBill.objects.select_related('checkbill').get(id=bill_id)
    else:
        checkbill=CheckBill(Creator=request.user)

    if request.method=='POST':
        p=request.POST.copy()

        if 'savedraft' in p:

            generate_form = CheckBillGenerateForm(request.POST)
            if generate_form.is_valid():
                formated_text=generate_form.cleaned_data['product_list']
                if not bill_id:
                    checkbill.save()
                checkbill.parse_detail_from_formated_text(formated_text)
                checkbill.save()

            #aa=reverse('checkbill_edit',args=[checkbill.id])
            checkbill.CheckState=CheckBill.CheckState_Choices[0][0]
            return HttpResponseRedirect(reverse('stockmanage:checkbill_edit',kwargs={'bill_id':str(checkbill.id)}))
        else:
            #import pdb;pdb.set_trace()
            for ks in p.keys():
                if ks.startswith('real_quantity_'):
                    detail_id=int(ks[14:])
                    detail=get_object_or_404(CheckBillDetail, pk=detail_id)
                    realquantity=int(p[ks])
                    detail.realquantity=realquantity
                    detail.save()
            if 'begin_input' in p:
                checkbill.CheckState=CheckBill.CheckState_Choices[1][0]
            elif 'complete' in p:
                #import pdb;pdb.set_trace()
                checkbill.CheckState=CheckBill.CheckState_Choices[2][0]
                # generate profit bill

                checkbill.CompleteCheck()
            # receive the realy quantity for each products.
            else:
                pass
        checkbill.save()
        return HttpResponseRedirect(reverse('stockmanage:checkbill_edit',kwargs={'bill_id':str(checkbill.id)}))

    else:
        #for billdetail in checkbill.stockbill_set.all():
        checkbilldetail_list=StockBillDetail.objects.filter(stockbill__id=bill_id).select_subclasses()
        #import pdb;pdb.set_trace()
        generate_form=CheckBillGenerateForm({'product_list':'\n'.join( checkbill.generat_detail_to_formatedtext())})
        detail_text=checkbill.generat_detail_to_formatedtext()
        return render(request,'stockmanage/checkbill_create_edit.html'
                      ,{'form':generate_form,'bill':checkbill,'detaillist':checkbilldetail_list})

        
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

