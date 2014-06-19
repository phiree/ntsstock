import django_tables2 as tables
from stockmanage.models import ProductStock
import itertools
class table2_productstock(tables.Table):
    row_number = tables.Column(empty_values=())
    class Meta:
        model=ProductStock
        sequence = ("row_number","product", "quantity", "stocklocation","memo")
        #attrs = {'class': 'table'}
    def __init__(self, *args, **kwargs):
        super(table2_productstock, self).__init__(*args, **kwargs)
        self.counter = itertools.count()
    def render_row_number(self):
        return 'Row %d' % next(self.counter)
