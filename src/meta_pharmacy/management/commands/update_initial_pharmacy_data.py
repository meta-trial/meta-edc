import sys

from django.core.management import BaseCommand

from meta_pharmacy.utils import update_initial_pharmacy_data


class Command(BaseCommand):
    def handle(self, *args, **options):  # noqa: ARG002
        update_initial_pharmacy_data()
        sys.stdout.write("Done\n")
