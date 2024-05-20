# Generated by Django 4.2.11 on 2024-05-15 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0196_glucosefbg_fbg_not_performed_reason_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="glucosefbg",
            name="fasting_duration_estimated",
            field=models.CharField(
                default="Yes",
                editable=False,
                help_text="Set to YES for existing values before duration question was added to the form, otherwise NO",
                max_length=15,
            ),
        ),
        migrations.AddField(
            model_name="historicalglucosefbg",
            name="fasting_duration_estimated",
            field=models.CharField(
                default="Yes",
                editable=False,
                help_text="Set to YES for existing values before duration question was added to the form, otherwise NO",
                max_length=15,
            ),
        ),
    ]
