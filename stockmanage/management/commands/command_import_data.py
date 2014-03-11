from django.core.management.base import BaseCommand, CommandError
from .data_importer import importer
import os
class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        print(os.path.dirname(os.path.realpath(__file__)))
        dir=os.path.dirname(os.path.realpath(__file__))+'\\files\\'
        for file in os.listdir(dir):
            print('开始导入:'+file)
            importer(dir+file).save_to_db()
            