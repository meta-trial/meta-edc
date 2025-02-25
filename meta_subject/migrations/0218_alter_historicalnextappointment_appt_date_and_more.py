# Generated by Django 6.0 on 2025-02-01 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0217_alter_historicalnextappointment_appt_datetime_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalnextappointment",
            name="appt_date",
            field=models.DateField(
                blank=True,
                help_text="Should fall on an valid clinic day for this facility",
                null=True,
                verbose_name="Next scheduled routine/facility appointment",
            ),
        ),
        migrations.AlterField(
            model_name="historicalnextappointment",
            name="appt_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Should fall on an valid clinic day for this facility",
                null=True,
                verbose_name="Next scheduled routine/facility appointment date and time",
            ),
        ),
        migrations.AlterField(
            model_name="nextappointment",
            name="appt_date",
            field=models.DateField(
                blank=True,
                help_text="Should fall on an valid clinic day for this facility",
                null=True,
                verbose_name="Next scheduled routine/facility appointment",
            ),
        ),
        migrations.AlterField(
            model_name="nextappointment",
            name="appt_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Should fall on an valid clinic day for this facility",
                null=True,
                verbose_name="Next scheduled routine/facility appointment date and time",
            ),
        ),
    ]
