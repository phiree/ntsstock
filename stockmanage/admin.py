from django.contrib import admin
from stockmanage.models import Product,Productlanguage,StockLocation
# Register your models here.
admin.site.register(Product)
admin.site.register(Productlanguage)
admin.site.register(StockLocation)

