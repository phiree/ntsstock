from django.forms import ModelForm
from stockmanage.models import StockBill
class StockBillForm(ModelForm):
    class Meta:
        model=StockBill