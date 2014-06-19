from django.template import Library
from model_utils.managers import InheritanceManager
register = Library()

@register.filter
def select_subclasses( value ):
    """
    base_instance|get_subclass
    """
    return value.select_subclasses()
