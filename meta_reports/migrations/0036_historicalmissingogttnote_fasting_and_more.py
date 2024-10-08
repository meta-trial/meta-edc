# Generated by Django 5.0.8 on 2024-08-23 14:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_reports", "0035_historicalmissingogttnote_missingogttnote"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalmissingogttnote",
            name="fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Did the participant fast?",
            ),
        ),
        migrations.AddField(
            model_name="historicalmissingogttnote",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="historicalmissingogttnote",
            name="fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long have they fasted in hours and/or minutes?",
            ),
        ),
        migrations.AddField(
            model_name="missingogttnote",
            name="fasting",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Did the participant fast?",
            ),
        ),
        migrations.AddField(
            model_name="missingogttnote",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="missingogttnote",
            name="fasting_duration_str",
            field=models.CharField(
                blank=True,
                help_text="As reported by patient. Duration of fast. Format is `HHhMMm`. For example 1h23m, 12h7m, etc",
                max_length=8,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{1,3}h([0-5]?[0-9]m)?)$",
                        message="Invalid format. Expected something like 1h20m, 11h5m, etc. No spaces allowed.",
                    )
                ],
                verbose_name="How long have they fasted in hours and/or minutes?",
            ),
        ),
    ]
