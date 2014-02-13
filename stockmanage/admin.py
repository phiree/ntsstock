from django.contrib import admin
from stockmanage.models import Product,Productlanguage,StockLocation,StockBill
# Register your models here.


class ProductLanguageInLine(admin.TabularInline):
    model=Productlanguage


class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductLanguageInLine]

admin.site.register(Product,ProductAdmin)
admin.site.register(StockLocation)
admin.site.register(StockBill)
