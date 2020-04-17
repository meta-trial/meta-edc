# Generated by Django 3.0.4 on 2020-04-17 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0018_coronakap_historicalcoronakap"),
    ]

    operations = [
        migrations.RenameField(
            model_name="coronakap", old_name="profession", new_name="employment",
        ),
        migrations.RenameField(
            model_name="coronakap",
            old_name="other_health_insurance",
            new_name="employment_other",
        ),
        migrations.RenameField(
            model_name="coronakap",
            old_name="other_profession",
            new_name="health_insurance_other",
        ),
        migrations.RenameField(
            model_name="coronakap",
            old_name="other_symptoms",
            new_name="symptoms_other",
        ),
        migrations.RenameField(
            model_name="historicalcoronakap",
            old_name="profession",
            new_name="employment",
        ),
        migrations.RenameField(
            model_name="historicalcoronakap",
            old_name="other_health_insurance",
            new_name="employment_other",
        ),
        migrations.RenameField(
            model_name="historicalcoronakap",
            old_name="other_profession",
            new_name="health_insurance_other",
        ),
        migrations.RenameField(
            model_name="historicalcoronakap",
            old_name="other_symptoms",
            new_name="symptoms_other",
        ),
    ]
