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
from django.views.generic import TemplateView
class about(TemplateView):
    template_name='stockmanage/about.html'
    company_name='NTS'