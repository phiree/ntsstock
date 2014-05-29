from stockmanage.models import StockBill,CheckBill,CheckBillDetail,ProductStock
from django.shortcuts import render,get_object_or_404,render_to_response
'''
盘点类.是否将盘点功能直接在
'''
class biz_check():
    def complete_check(self,checkbill):

        list_change=checkbill.GenerateChangeDetail()
        if len(list_change)>0:

            check_stockin_bill = StockBill(BillType='in', BillState='applied',
                                       StaffName=checkbill.StaffName, Creator=checkbill.Creator,RelatedBill=checkbill,
                                       BillReason='inventory_profit')
            check_stockout_bill = StockBill(BillType='out', BillState='applied',RelatedBill=checkbill,
                                       StaffName=checkbill.StaffName, Creator=checkbill.Creator,
                                       BillReason='inventory_loss')
            check_stockin_bill.save()
            check_stockout_bill.save()
            for change in list_change:
                #import pdb;pdb.set_trace()
                #update productstock
                ps=get_object_or_404(ProductStock,stocklocation=change.location,theproduct=change.product)
                ps.quantity+=change.quantity
                ps.save()
                if change.quantity>0:
                    change.stockbill=check_stockin_bill
                else:
                    change.quantity*=-1
                    change.stockbill=check_stockout_bill
                change.save()



