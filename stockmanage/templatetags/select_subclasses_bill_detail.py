from django.template import Library
from model_utils.managers import InheritanceManager
from stockmanage.models  import BillDetailBase
register = Library()

@register.filter
def select_subclasses_bill_detail( value ):
    """
    base_instance|get_subclass
    """

    return BillDetailBase.objects.filter(billbase=value).select_subclasses()
