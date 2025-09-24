import sys

from django.core.management import BaseCommand

from meta_analytics.dataframes import GlucoseEndpointsByDate


class Command(BaseCommand):
    def handle(self, *args, **options):  # noqa: ARG002
        sys.stdout.write("Generating endpoints...\n")
        cls = GlucoseEndpointsByDate()
        cls.run()
        cls.to_model()
        sys.stdout.write("Generating endpoints... done.\n")
