# Generated by Django 3.2.13 on 2022-09-28 01:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0153_auto_20220928_0250"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalstudymedication",
            name="next_dosage_guideline",
        ),
        migrations.RemoveField(
            model_name="historicalstudymedication",
            name="next_formulation",
        ),
        migrations.RemoveField(
            model_name="historicalstudymedication",
            name="order_or_update_next",
        ),
        migrations.RemoveField(
            model_name="studymedication",
            name="next_dosage_guideline",
        ),
        migrations.RemoveField(
            model_name="studymedication",
            name="next_formulation",
        ),
        migrations.RemoveField(
            model_name="studymedication",
            name="order_or_update_next",
        ),
    ]