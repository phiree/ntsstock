from django.conf.urls import patterns,url
from stockmanage import views

urlpatterns=patterns(''
                     
                     ,url(r'^stocklocation/',views.location_index,name='stocklocation_index' )
                     ,url(r'^locationmanage/',views.location_manage,name='location_manage' )
                     ,url(r'^$',views.index,name='index')
                     )
