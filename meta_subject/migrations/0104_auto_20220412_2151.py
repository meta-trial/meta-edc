# Generated by Django 3.2.11 on 2022-04-12 18:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meta_subject", "0103_auto_20220324_0326"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalstudymedication",
            name="refill_to_next_visit",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=25,
                verbose_name="Refill to the next scheduled visit",
            ),
        ),
        migrations.AddField(
            model_name="studymedication",
            name="refill_to_next_visit",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="Yes",
                max_length=25,
                verbose_name="Refill to the next scheduled visit",
            ),
        ),
    ]
