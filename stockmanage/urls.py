from django.conf.urls import patterns,url
from stockmanage import views

urlpatterns=patterns(''
                     
                     ,url(r'^stocklocation/',views.location_index,name='stocklocation_index' )
                     ,url(r'^location_add_modify/',views.location_add_modify,name='location_add_modify' )
                     ,url(r'^location_get/(?P<location_id>\d+)$',views.location_get,name='location_get' )
                     ,url(r'^location_delete/(?P<location_id>\d+)$',views.location_delete,name='location_delete' )
                     
                     ,url(r'^stockbill/list/all/',views.stockbill_list,name='stockbill_list' )
                     ,url(r'^stockbill/in/',views.stockbill_in_index,name='stockbill_in_index' )
                     ,url(r'^stockbill/create/',views.stockbill_create,name='stockbill_create' )
                     ,url(r'^stockbill/edit/(?P<bill_id>[^/]+)/',views.stockbill_edit,name='stockbill_edit' )
                     ,url(r'^stockbill/update_detail/(?P<bill_id>[^/]+)/',views.stockbill_update_detail,name='stockbill_update_detail' )
                     
                     ,url(r'^$',views.index,name='index')
                     )
