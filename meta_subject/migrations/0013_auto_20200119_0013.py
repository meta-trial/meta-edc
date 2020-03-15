# Generated by Django 2.2.7 on 2020-01-18 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0012_auto_20200118_2334"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalmalariatest",
            name="diagnostic_type",
            field=models.CharField(
                choices=[
                    ("rapid_test", "Rapid test"),
                    ("microscopy", "Microscopy"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="Diagnostic test used",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmalariatest",
            name="performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Was the malaria test performed?",
            ),
        ),
        migrations.AlterField(
            model_name="malariatest",
            name="diagnostic_type",
            field=models.CharField(
                choices=[
                    ("rapid_test", "Rapid test"),
                    ("microscopy", "Microscopy"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=15,
                verbose_name="Diagnostic test used",
            ),
        ),
        migrations.AlterField(
            model_name="malariatest",
            name="performed",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Was the malaria test performed?",
            ),
        ),
    ]