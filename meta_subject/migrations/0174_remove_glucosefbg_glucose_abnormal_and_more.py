# Generated by Django 5.0.1 on 2024-02-14 03:27

import django.core.validators
import edc_model.validators.date
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0173_alter_glucosefbg_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="glucosefbg",
            name="glucose_abnormal",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="glucose_grade",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="glucose_grade_description",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="glucose_reportable",
        ),
        migrations.RemoveField(
            model_name="glucosefbg",
            name="is_poc",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="glucose_abnormal",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="glucose_grade",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="glucose_grade_description",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="glucose_reportable",
        ),
        migrations.RemoveField(
            model_name="historicalglucosefbg",
            name="is_poc",
        ),
        migrations.AlterField(
            model_name="glucosefbg",
            name="assay_datetime",
            field=models.DateTimeField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.datetime_not_future],
                verbose_name="Result date and time",
            ),
        ),
        migrations.AlterField(
            model_name="glucosefbg",
            name="glucose_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1.0),
                    django.core.validators.MaxValueValidator(9999.99),
                ],
                verbose_name="FBG",
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucosefbg",
            name="assay_datetime",
            field=models.DateTimeField(
                blank=True,
                null=True,
                validators=[edc_model.validators.date.datetime_not_future],
                verbose_name="Result date and time",
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucosefbg",
            name="glucose_value",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                max_digits=8,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1.0),
                    django.core.validators.MaxValueValidator(9999.99),
                ],
                verbose_name="FBG",
            ),
        ),
    ]
