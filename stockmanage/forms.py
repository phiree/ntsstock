from django import forms
from django.forms import ModelForm
from stockmanage.models import StockBill
class StockBillForm(ModelForm):
    #BillTime=forms.DateTimeFiled(widget=forms.DateInput(attrs={'class':'timepicker'}),required=True)
    BillNo=forms.CharField(label='入库单号')
    #BillReason=forms.ChoiceField()
    def __init__(self, *args, **kwargs):
        super(StockBillForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        #import pdb; pdb.set_trace()
        self.fields['BillReason']=forms.CharField(max_length=100,label='原因',
                                                  widget=forms.Select(
                                                choices=StockBill.Reason_Choices[0 if instance.BillType=='in' else 1][1]))
        self.fields['TotalAmount'].widget.attrs['readonly'] = True
        self.fields['TotalKinds'].widget.attrs['readonly'] = True
        if instance and  instance.BillState!=instance.state_draft:
            #pass
            self.fields['BillNo'].widget.attrs['readonly'] = True
            self.fields['BillReason'].widget.attrs['disabled'] ='disabled'
            
            self.fields['Memo'].widget.attrs['readonly'] = True
            self.fields['StaffName'].widget.attrs['readonly'] = True
    class Media:
        js=('stockbill.js',)
        css={'all':('css/stockbill.css',)}
      
    def clean_BillNo(self):
        instance = getattr(self, 'instance', None)
        if instance and  instance.BillState!=instance.state_draft:
            return instance.BillNo
        else:
            return self.cleaned_data['BillNo']
     
    def clean_BillReason(self):
        #import pdb;pdb.set_trace()
        instance = getattr(self, 'instance', None)
        if instance and  instance.BillState!=instance.state_draft:
            return instance.BillReason
        else:
            return self.cleaned_data['BillReason']
        
    def clean_Memo(self):
        instance = getattr(self, 'instance', None)
        if instance and  instance.BillState!=instance.state_draft:
            return instance.Memo
        else:
            return self.cleaned_data['Memo']
    def clean_StaffName(self):
        instance = getattr(self, 'instance', None)
        if instance and  instance.BillState!=instance.state_draft:
            return instance.StaffName
        else:
            return self.cleaned_data['StaffName']
    class Meta:
        model=StockBill
        fields =['BillNo','BillReason','TotalAmount','TotalKinds','Memo','StaffName']