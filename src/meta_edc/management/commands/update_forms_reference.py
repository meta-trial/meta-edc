import sys

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.color import color_style
from edc_form_describer.forms_reference import FormsReference

from meta_subject.admin_site import meta_subject_admin
from meta_visit_schedule.visit_schedules import visit_schedule

style = color_style()


def update_forms_reference(sender=None, **kwargs):  # noqa: ARG001
    sys.stdout.write(
        style.MIGRATE_HEADING("Refreshing CRF reference document for meta_subject\n")
    )
    doc_folder = settings.BASE_DIR / "docs"
    if not doc_folder.exists():
        doc_folder.mkdir()
    forms = FormsReference(
        visit_schedules=[visit_schedule],
        admin_site=meta_subject_admin,
        add_per_form_timestamp=False,
    )
    path = doc_folder / "forms_reference.md"
    forms.to_file(path=path, overwrite=True, pad=0)


class Command(BaseCommand):
    help = "Update forms reference document (.md)"

    def handle(self, *args, **options):  # noqa: ARG002
        update_forms_reference()
