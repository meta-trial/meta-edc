# Generated by Django 2.2.6 on 2019-10-21 02:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("meta_subject", "0002_auto_20191021_0353")]

    operations = [
        migrations.AlterField(
            model_name="followupvitals",
            name="oxygen_saturation",
            field=models.IntegerField(
                help_text="%",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999),
                ],
                verbose_name="Oxygen saturation:",
            ),
        ),
        migrations.AlterField(
            model_name="followupvitals",
            name="respiratory_rate",
            field=models.IntegerField(
                help_text="breaths/min",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(6),
                    django.core.validators.MaxValueValidator(50),
                ],
                verbose_name="Respiratory rate:",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowupvitals",
            name="oxygen_saturation",
            field=models.IntegerField(
                help_text="%",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999),
                ],
                verbose_name="Oxygen saturation:",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowupvitals",
            name="respiratory_rate",
            field=models.IntegerField(
                help_text="breaths/min",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(6),
                    django.core.validators.MaxValueValidator(50),
                ],
                verbose_name="Respiratory rate:",
            ),
        ),
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="oxygen_saturation",
            field=models.IntegerField(
                help_text="%",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999),
                ],
                verbose_name="Oxygen saturation:",
            ),
        ),
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="respiratory_rate",
            field=models.IntegerField(
                help_text="breaths/min",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(6),
                    django.core.validators.MaxValueValidator(50),
                ],
                verbose_name="Respiratory rate:",
            ),
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="oxygen_saturation",
            field=models.IntegerField(
                help_text="%",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(999),
                ],
                verbose_name="Oxygen saturation:",
            ),
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="respiratory_rate",
            field=models.IntegerField(
                help_text="breaths/min",
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(6),
                    django.core.validators.MaxValueValidator(50),
                ],
                verbose_name="Respiratory rate:",
            ),
        ),
    ]