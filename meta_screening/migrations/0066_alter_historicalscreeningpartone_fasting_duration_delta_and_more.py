# Generated by Django 4.2.11 on 2024-05-16 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_screening", "0065_auto_20240516_0352"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True,
                help_text="system calculated to microseconds. (hours=microseconds/3.6e+9)",
                null=True,
            ),
        ),
    ]
