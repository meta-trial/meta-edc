# Generated by Django 5.0.1 on 2024-02-07 23:59
from uuid import uuid4

from django.db import migrations
from django.db.migrations import RunPython
from tqdm import tqdm


def update_duplicate_rx_identifier(apps, schema_editor):
    rx_model_cls = apps.get_model("edc_pharmacy.rx")
    qs = rx_model_cls.objects.filter(rx_identifier="0817ce95-fdc5-426b-9d4d-08fb717de2a6")
    for obj in tqdm(qs, total=qs.count()):
        obj.rx_identifier = uuid4()
        obj.save_base(update_fields="rx_identifier")
    rx_model_cls = apps.get_model("edc_pharmacy.historicalrx")
    qs = rx_model_cls.objects.filter(rx_identifier="0817ce95-fdc5-426b-9d4d-08fb717de2a6")
    for obj in tqdm(qs, total=qs.count()):
        obj.rx_identifier = uuid4()
        obj.save_base(update_fields="rx_identifier")


class Migration(migrations.Migration):
    dependencies = [
        (
            "edc_pharmacy",
            "0020_alter_box_device_created_alter_box_device_modified_and_more",
        )
    ]

    # ran this in shell manually 2024/02/13
    # operations = [RunPython(update_duplicate_rx_identifier)]
    operations = []