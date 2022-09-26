# Generated by Django 3.2.13 on 2022-09-06 23:02

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0144_auto_20220907_0157"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalstudymedication",
            name="refill_identifier",
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36),
        ),
        migrations.AddField(
            model_name="studymedication",
            name="refill_identifier",
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36),
        ),
        migrations.AlterField(
            model_name="historicalstudymedication",
            name="order_or_update_next",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Order, or update, refill for next scheduled visit?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalstudymedication",
            name="refill_start_datetime",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="studymedication",
            name="order_or_update_next",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=15,
                verbose_name="Order, or update, refill for next scheduled visit?",
            ),
        ),
        migrations.AlterField(
            model_name="studymedication",
            name="refill_start_datetime",
            field=models.DateTimeField(),
        ),
    ]