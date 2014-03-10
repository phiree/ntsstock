from django.test import TestCase
from read_excel_to_list import excel_reader
class readtest(TestCase):
    
    def test_read_excel_with_combined_cols_and_rows(self):
        
        