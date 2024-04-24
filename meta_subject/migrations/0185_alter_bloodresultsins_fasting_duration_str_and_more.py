# Generated by Django 5.0.4 on 2024-04-18 23:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0184_alter_glucose_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodresultsins",
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
        migrations.AlterField(
            model_name="glucose",
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
        migrations.AlterField(
            model_name="historicalbloodresultsins",
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
        migrations.AlterField(
            model_name="historicalglucose",
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