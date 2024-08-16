from django.core.management import BaseCommand

from meta_analytics.dataframes import GlucoseEndpointsByDate


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Generating endpoints...")
        cls = GlucoseEndpointsByDate()
        cls.run()
        cls.to_model()
        print("Generating endpoints... done.")
