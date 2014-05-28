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
from stockmanage.forms import StockBillForm,CheckBillGenerateForm,InitImportForm
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.forms.models import inlineformset_factory
from django.views.generic import View,ListView,TemplateView
import xlrd
from .data_importer import importer
'''
bill list views
'''
class ViewInitImport(TemplateView):
    template_name='init_import.html'
    
    

def importdata(request):
    if request.method=='GET':
        return render(request,'stockmanage/init_import.html',{'form':InitImportForm()})
    elif request.method=='POST':
        form = InitImportForm(request.POST, request.FILES)
        initdata=importer(request.FILES['file'].read())
        initdata.save_to_db()
        
        return render(request,'stockmanage/about.html')
    else:
        return null