from django.contrib import admin
from django.http import HttpResponseRedirect
from stockmanage.models import Product,StockLocation,StockBill,StockBillDetail,ProductStock
# Register your models here.



class StockBillDetailInline(admin.TabularInline):
    model=StockBillDetail
    fields=('product',)
    readonly_fields=('product','location','quantity',)
    template='admin/stockmanage/stockbill/edit_inline/tabular.html' 
class ProductAdmin(admin.ModelAdmin):
  pass

class StockLocationAdmin(admin.ModelAdmin):
    
    
        
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['all_top_locations']=StockLocation.objects.filter(ParentLocation=None)
        return super(StockLocationAdmin, self).changelist_view(request,extra_context=extra_context)
    class Media:
        css = {
            "all": (
                    'stockmanage/jquery/jqueryui/themes/base/jquery-ui.css',
                    'stockmanage/css/showroommanage.css')
        }
        '''BUG IN JQUERY?'''
        js = (
              
              'stockmanage/jquery/jquery-1.6.4.min.js',
              'stockmanage/jquery/jqueryui/jquery-ui-1.10.3.min.js'
              ,'stockmanage/jquery/plugin/jquery.cookie.js'
              ,'stockmanage/js/locationservice.js'
              ,
              )
        
class StockBillDetailAdmin(admin.ModelAdmin):
   pass
    
    
class StockBillAdmin(admin.ModelAdmin):
    list_filter=('BillType','BillState','BillTime')
    inlines=[StockBillDetailInline]
    #fields=('BillTime','BillType','TotalAmount','TotalKinds','BillState','StaffName','Memo') 
    list_display =('BillNo','Creator','BillTime','BillType','TotalAmount','TotalKinds','BillState','StaffName','Memo')
    
    def detail_link_column(self,obj):
        return '<a href="google.com">Details</a>'
    detail_link_column.allow_tags=True
    detail_link_column.short_description='View Bill Details'
    
    radio_fields={'BillType':admin.HORIZONTAL}
    
    readonly_fields=('TotalAmount','TotalKinds')
    fieldsets = (
        (None, {
            'fields': (('BillNo', 'BillTime'), ('BillType','BillReason'),('TotalAmount','TotalKinds'))
        }), 
    )
    
    def save_model(self, request, obj, form, change):
        obj.Creator = request.user
        obj.stockbilldetail_set.clear()
        #import pdb;pdb.set_trace()
        plain_list= request.POST['tt_detail_plain_list']
        for line in plain_list.splitlines():
            if not line:
                continue
            procode=line.split(',')[0]
            product=Product.objects.get(NTSCode=procode)
            qty=line.split(',')[1]
            location_code=line.split(',')[2]
            location=StockLocation.objects.get(LocationCode=location_code)
            detail=StockBillDetail(stockbill=obj,product=product,location=location,quantity=qty)
            obj.stockbilldetail_set.add(detail)
            #import pdb;pdb.set_trace()
        obj.save()
    #actions_on_bottom = True
    #list_filter=
    #templates
    #add_form_template='admin/stockmanage/stockbill/add.html'
  
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if not self.get_object(request, object_id).BillState=='draft':
            self.readonly_fields=('TotalAmount','TotalKinds','BillType')
        return super(StockBillAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

class ProductStockAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product,ProductAdmin)
admin.site.register(StockLocation,StockLocationAdmin)
admin.site.register(StockBill,StockBillAdmin)
#admin.site.register(StockBillDetail,StockBillDetailAdmin)
admin.site.register(ProductStock,ProductStockAdmin)

