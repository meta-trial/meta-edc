# Generated by Django 5.0.8 on 2024-08-21 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0210_remove_dmdxresult_dm_diagnosis_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dmendpoint",
            name="endpoint_reached",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If YES, the EDC will check for the patient on the Endpoints report.",
                max_length=15,
                null=True,
                verbose_name="Was the patient referred because the diabetes endpoint was reached?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldmendpoint",
            name="endpoint_reached",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If YES, the EDC will check for the patient on the Endpoints report.",
                max_length=15,
                null=True,
                verbose_name="Was the patient referred because the diabetes endpoint was reached?",
            ),
        ),
        migrations.AlterField(
            model_name="dmendpoint",
            name="dx_date",
            field=models.DateField(null=True, verbose_name="Date endpoint reached"),
        ),
        migrations.AlterField(
            model_name="historicaldmendpoint",
            name="dx_date",
            field=models.DateField(null=True, verbose_name="Date endpoint reached"),
        ),
    ]