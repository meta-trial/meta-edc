# Generated by Django 5.1.2 on 2024-10-14 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_pharmacy", "0008_historicallabeldata_labeldata"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicallabeldata",
            name="batch",
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="labeldata",
            name="batch",
            field=models.CharField(max_length=15, null=True),
        ),
    ]
