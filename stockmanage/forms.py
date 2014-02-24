from django import forms
from django.forms import ModelForm
from stockmanage.models import StockBill
class StockBillForm(ModelForm):
    #BillTime=forms.DateTimeFiled(widget=forms.DateInput(attrs={'class':'timepicker'}),required=True)
    def __init__(self, *args, **kwargs):
        super(StockBillForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #import pdb; pdb.set_trace()
        self.fields['TotalAmount'].widget.attrs['readonly'] = True
        self.fields['TotalKinds'].widget.attrs['readonly'] = True
        if instance and  instance.BillState!=instance.state_draft:
            #pass
            self.fields['BillNo'].widget.attrs['readonly'] = True
    class Media:
        js=('stockbill.js',)
        
                
    def clean_BillNo(self):
        instance = getattr(self, 'instance', None)
        if instance and  instance.BillState!=instance.state_draft:
            return instance.BillNo
        else:
            return self.cleaned_data['BillNo']
    class Meta:
        model=StockBill
        fields =['BillNo', 'BillType','BillReason','TotalAmount','TotalKinds']