from django.utils import timezone
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import  reverse
from django.views import generic
# Create your views here.
def index(request):
    return render(request,'stockmanage/index.html')

