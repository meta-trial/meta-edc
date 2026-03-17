import sys

from clinicedc_constants import NULL_STRING
from django.apps import apps as django_apps
from django.core.management import BaseCommand
from django.db.models import Count
from edc_qareports.models import Note
from tqdm import tqdm


class Command(BaseCommand):
    def handle(self, *args, **options):  # noqa: ARG002
        sys.stdout.write("Updating visit_code on Note model...\n")
        for report_models in (
            Note.objects.values("report_model").annotate(total=Count("id")).order_by()
        ):
            sys.stdout.write(f"{report_models.get('report_model')}\n")
            model_cls = django_apps.get_model(report_models.get("report_model"))
            report_query = model_cls.objects.exclude(visit_code__isnull=True)
            for report_obj in tqdm(report_query, total=report_query.count()):
                try:
                    note_obj = Note.objects.get(
                        report_model=model_cls._meta.label_lower,
                        subject_identifier=report_obj.subject_identifier,
                        visit_code=NULL_STRING,
                    )
                except Note.DoesNotExist:
                    pass
                else:
                    note_obj.visit_code = report_obj.visit_code or NULL_STRING
                    note_obj.visit_code_sequence = report_obj.visit_code_sequence or 0
                    note_obj.save()

        sys.stdout.write("Done.\n")
