from django.conf.urls import patterns,url
from stockmanage import views,views_productstock,views_checkbill,views_product,views_init
from stockmanage.views_about import about
from django.views.generic import  TemplateView
from stockmanage.views_checkbill import CheckBillList
from stockmanage.views_bill import BillListView,BillDetailView
from stockmanage.views_productstock import ProductStockList,StockTraceList
from stockmanage.views_init import ViewInitImport
urlpatterns=patterns(''
                     ,url(r'^about/',TemplateView.as_view(template_name='stockmanage/about.html'))
                     ,url(r'^stocklocation/',views.location_index,name='stocklocation_index' )
                     ,url(r'^location_add_modify/',views.location_add_modify,name='location_add_modify' )
                     ,url(r'^location_get/(?P<location_id>\d+)$',views.location_get,name='location_get' )
                     ,url(r'^location_delete/(?P<location_id>\d+)$',views.location_delete,name='location_delete' )
                     #单据列表
                     ,url(r'^bill/list[/]$',BillListView.as_view(template_name='stockmanage/billbase_list.html'),name='bill_list' )
                     ,url(r'^bill/list/(?P<billtype>[^/]+)/',BillListView.as_view(template_name='stockmanage/billbase_list.html'),name='bill_list' )
                     ,url(r'^bill/detail/(?P<pk>[^/]+)/',BillDetailView.as_view(template_name='stockmanage/billbase_detail.html'),name='bill_detail' )

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
                     ,url(r'^productstock/list/',ProductStockList.as_view(paginate_by=20),name='productstock_list' )
                     ,url(r'^productstock/stock_trace/(?P<product_id>[^/]+)/',StockTraceList.as_view(template_name='stockmanage/stocktrace_list.html'),name='productstock_stocktrace_list')
                     #######盘点##############
                     #盘点计划列表
                     ,url(r'^checkbill/list/',CheckBillList.as_view(),name='checkbill_list')
                     ,url(r'^checkbill/create/',views_checkbill.edit,name='checkbill_create')
                     #,url(r'^checkbill/list',views_checkbill.list,name='checkbill_list')
                     #创建盘点单
                     ,url(r'^checkbill/edit/(?P<bill_id>[^/]+)/',views_checkbill.edit,name='checkbill_edit')
                     #编辑盘点清单(增加,删除盘点目标)
                     ,url(r'^checkbill/input_realquantity/(?P<bill_id>[^/]+)/',views_checkbill.input_realquantity,name='checkbill_input_realquantity')
                     #产品详情
                     ,url(r'^product/detail/(?P<product_id>[^/]+)/',views_product.detail,name='product_detail')
                     ,url(r'^init_importdata/',views_init.importdata,name='init_importdata')
                     ,url(r'^user_manual/',TemplateView.as_view(template_name='stockmanage/user_manual.html'),name='user_manual')
                     ,url(r'^$',views.index,name='index')
                     ,
                     )
                     