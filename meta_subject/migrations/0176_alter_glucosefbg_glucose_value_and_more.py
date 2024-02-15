# Generated by Django 5.0.1 on 2024-02-15 06:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0175_auto_20240214_2239"),
    ]

    operations = [
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
                verbose_name="Glucose",
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
                verbose_name="Glucose",
            ),
        ),
    ]
