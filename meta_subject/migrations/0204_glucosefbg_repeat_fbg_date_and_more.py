# Generated by Django 4.2.11 on 2024-05-16 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0203_alter_bloodresultsins_fasting_duration_delta_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="glucosefbg",
            name="repeat_fbg_date",
            field=models.DateField(
                blank=True, help_text="Date should be within 1 week of report date", null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalglucosefbg",
            name="repeat_fbg_date",
            field=models.DateField(
                blank=True, help_text="Date should be within 1 week of report date", null=True
            ),
        ),
    ]
