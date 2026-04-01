import sys

from django.core.management import BaseCommand

from meta_analytics.dataframes import GlucoseEndpointsByDate2
from meta_reports.models import Endpoints


class Command(BaseCommand):
    def handle(self, *args, **options):  # noqa: ARG002
        sys.stdout.write("Generating endpoints...\n")
        cls = GlucoseEndpointsByDate2()
        cls.to_model()
        record_count = Endpoints.objects.all().count()
        sys.stdout.write(
            f"{record_count} endpoints. See table {Endpoints._meta.verbose_name}. Done.\n"
        )
