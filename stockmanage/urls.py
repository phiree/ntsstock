from django.conf.urls import patterns,url
from stockmanage import views,views_productstock,views_checkbill,views_product

urlpatterns=patterns(''
                     ,url(r'^stocklocation/',views.location_index,name='stocklocation_index' )
                     ,url(r'^location_add_modify/',views.location_add_modify,name='location_add_modify' )
                     ,url(r'^location_get/(?P<location_id>\d+)$',views.location_get,name='location_get' )
                     ,url(r'^location_delete/(?P<location_id>\d+)$',views.location_delete,name='location_delete' )
                     #入库单
                     ,url(r'^stockbill/stockin/list/',views.stockbill_stockin_list,name='stockbill_stockin_list' )
                     #出库单
                     ,url(r'^stockbill/stockout/list/',views.stockbill_stockout_list,name='stockbill_stockout_list' )
                      #新建入库
                     ,url(r'^stockbill/stockin/create',views.stockbill_stockin_create,name='stockbill_stockin_create' )
                     #新建出库
                     ,url(r'^stockbill/stockout/create',views.stockbill_stockout_create,name='stockbill_stockout_create' )
                     #编辑入库单
                     ,url(r'^stockbill/stockin/edit/(?P<bill_id>[^/]+)/',views.stockbill_stockin_edit,name='stockbill_stockin_edit' )
                     #编辑出库单
                     ,url(r'^stockbill/stockout/edit/(?P<bill_id>[^/]+)/',views.stockbill_stockout_edit,name='stockbill_stockout_edit' )
                     #编辑单据详情
                     ,url(r'^stockbill/update_detail/(?P<bill_id>[^/]+)/',views.stockbill_update_detail,name='stockbill_update_detail' )
                     #库存清单
                     ,url(r'^productstock/list',views_productstock.list,name='productstock_list' )
                     ,url(r'productstock/stock_trace/(?P<product_id>[^/]+)/',views_productstock.stock_trace_list,name='productstock_stocktrace_list')
                     #######盘点##############
                     #盘点计划列表
                     ,url(r'^checkbill/$',views_checkbill.list,name='checkbill_list')
                     #,url(r'^checkbill/list',views_checkbill.list,name='checkbill_list')
                     #创建盘点单
                     ,url(r'^checkbill/create',views_checkbill.create,name='checkbill_create')
                     #编辑盘点清单(增加,删除盘点目标)
                     ,url(r'^checkbill/edit/(?P<bill_id>[^/]+)/',views_checkbill.edit,name='checkbill_edit')
                     #产品详情
                    ,url(r'^product/detail/(?P<product_id>[^/]+)/',views_product.detail,name='product_detail')
                     ,url(r'^$',views.index,name='index')
                     )
