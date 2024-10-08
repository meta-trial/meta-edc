# Generated by Django 4.1.2 on 2022-11-30 19:57
from django.core.exceptions import ObjectDoesNotExist
from django.db import migrations
from edc_constants.constants import NOT_APPLICABLE
from tqdm import tqdm


def update_investigator_ae_classification(apps, schema_editor):
    ae_tmg_cls = apps.get_model("meta_ae", "aetmg")
    ae_classification_cls = apps.get_model("edc_adverse_event", "aeclassification")
    try:
        ae_classification = ae_classification_cls.objects.get(name=NOT_APPLICABLE)
    except ObjectDoesNotExist:
        pass
    else:
        total = ae_tmg_cls.objects.filter(investigator_ae_classification__isnull=True).count()
        for obj in tqdm(
            ae_tmg_cls.objects.filter(investigator_ae_classification__isnull=True), total=total
        ):
            obj.investigator_ae_classification = ae_classification
            obj.save_base(update_fields=["investigator_ae_classification"])


class Migration(migrations.Migration):
    dependencies = [
        ("meta_ae", "0016_rename_narrative_aetmg_investigator_narrative_and_more"),
    ]

    operations = [migrations.RunPython(update_investigator_ae_classification)]
