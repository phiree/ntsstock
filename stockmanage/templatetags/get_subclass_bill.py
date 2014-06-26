from django.template import Library
from model_utils.managers import InheritanceManager
from stockmanage.models import BillBase
register = Library()

@register.filter
def get_subclass_bill( value ):
    """
    base_instance|get_subclass
    """
    return BillBase.objects.get_subclass(pk=value.id)
