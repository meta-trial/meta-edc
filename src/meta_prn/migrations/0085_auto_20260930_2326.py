from clinicedc_constants import CONSENT_WITHDRAWAL

from django.db import migrations
from edc_offstudy.constants import WITHDRAWAL
from meta_lists.models import OffstudyReasons


def update_consent_withdrawal(apps, schema_editor):
    OffstudyReasons.objects.filter(name=WITHDRAWAL).update(name=CONSENT_WITHDRAWAL)


class Migration(migrations.Migration):

    dependencies = [
        ("meta_prn", "0084_endofstudy_clinical_withdrawal_date_and_more"),
    ]

    operations = [migrations.RunPython(update_consent_withdrawal)]
