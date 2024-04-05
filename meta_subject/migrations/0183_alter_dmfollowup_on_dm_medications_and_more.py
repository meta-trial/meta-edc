# Generated by Django 4.2.11 on 2024-04-05 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0182_rename_dmreferralfollowup_dmfollowup_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dmfollowup",
            name="on_dm_medications",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=25,
                verbose_name="Are you currently taking any drug therapy for diabetes?",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldmfollowup",
            name="on_dm_medications",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=25,
                verbose_name="Are you currently taking any drug therapy for diabetes?",
            ),
        ),
    ]
