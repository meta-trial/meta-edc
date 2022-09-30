# Generated by Django 3.2.13 on 2022-09-27 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0152_auto_20220925_0509"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalstudymedication",
            name="refill",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                help_text="If NO, set refill_start_datetime equal to the refill_end_datetime",
                max_length=15,
                verbose_name="Will the subject receive study medication for this visit",
            ),
        ),
        migrations.AddField(
            model_name="studymedication",
            name="refill",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                help_text="If NO, set refill_start_datetime equal to the refill_end_datetime",
                max_length=15,
                verbose_name="Will the subject receive study medication for this visit",
            ),
        ),
    ]