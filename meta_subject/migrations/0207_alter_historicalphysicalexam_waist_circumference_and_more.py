# Generated by Django 4.2.11 on 2024-06-10 19:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0206_bloodresultsfbc_crf_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="waist_circumference",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                help_text="in centimeters",
                max_digits=5,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(50.0),
                    django.core.validators.MaxValueValidator(175.0),
                ],
                verbose_name="Waist circumference",
            ),
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="waist_circumference",
            field=models.DecimalField(
                blank=True,
                decimal_places=1,
                help_text="in centimeters",
                max_digits=5,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(50.0),
                    django.core.validators.MaxValueValidator(175.0),
                ],
                verbose_name="Waist circumference",
            ),
        ),
    ]
