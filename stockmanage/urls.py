from django.conf.urls import patterns,url
from stockmanage import views

urlpatterns=patterns(''
                     ,url(r'^$',views.index,name='index')
                     )
