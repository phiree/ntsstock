from django.core.management.base import BaseCommand, CommandError
from .data_importer import importer
import os
class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        dir=r'F:\Work\NTS\ntsstock\stockmanage\management\commands\files\\'
        for file in os.listdir(dir):
            importer(dir+file).save_to_db()
            