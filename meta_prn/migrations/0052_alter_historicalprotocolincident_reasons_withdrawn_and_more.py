# Generated by Django 4.1.2 on 2022-11-30 22:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meta_prn", "0051_historicalprotocolincident_reasons_withdrawn_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalprotocolincident",
            name="reasons_withdrawn",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="protocolincident",
            name="reasons_withdrawn",
            field=models.TextField(blank=True, null=True),
        ),
    ]