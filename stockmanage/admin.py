from django.contrib import admin
from stockmanage.models import Product,Productlanguage,StockLocation,StockBill,StockBillDetail,ProductStock
# Register your models here.


class ProductLanguageInLine(admin.TabularInline):
    model=Productlanguage
class StockBillDetailInline(admin.TabularInline):
    model=StockBillDetail

class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductLanguageInLine]

class StockLocationAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['all_top_locations']=StockLocation.objects.filter(ParentLocation=None)
        return super(StockLocationAdmin, self).changelist_view(request,extra_context=extra_context)

class StockBillAdmin(admin.ModelAdmin):
    inlines=[StockBillDetailInline]
    #fields=('BillTime','BillType','TotalAmount','TotalKinds','BillState','StaffName','Memo') 
    list_display =('BillTime','BillType','TotalAmount','TotalKinds','BillState','StaffName','Memo')
    def detail_link_column(self,obj):
        return '<a href="google.com">Details</a>'
    detail_link_column.allow_tags=True
    detail_link_column.short_description='View Bill Details'
    #list_filter=
class ProductStockAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product,ProductAdmin)
admin.site.register(StockLocation,StockLocationAdmin)
admin.site.register(StockBill,StockBillAdmin)
admin.site.register(ProductStock,ProductStockAdmin)

