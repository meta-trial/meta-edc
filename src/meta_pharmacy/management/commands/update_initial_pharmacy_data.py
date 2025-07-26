from django.core.management import BaseCommand

from meta_pharmacy.utils import update_initial_pharmacy_data


class Command(BaseCommand):

    def handle(self, *args, **options):
        update_initial_pharmacy_data()
        print("Done")
