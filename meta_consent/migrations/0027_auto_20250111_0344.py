# Generated by Django 5.1.2 on 2025-01-11 00:44

from django.db import IntegrityError, migrations, transaction
from edc_registration.models import RegisteredSubject
from tqdm import tqdm

from meta_consent.action_items import ConsentV1ExtensionAction


def update_action_item(apps, schema_editor):
    total = RegisteredSubject.objects.all().count()
    for obj in tqdm(RegisteredSubject.objects.all(), total=total):
        try:
            with transaction.atomic():
                ConsentV1ExtensionAction(
                    subject_identifier=obj.subject_identifier,
                    skip_get_current_site=True,
                    site_id=obj.site_id,
                )
        except IntegrityError:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ("meta_consent", "0026_historicalsubjectconsentv1ext_subjectconsentv1ext"),
    ]

    operations = [migrations.RunPython(update_action_item)]
