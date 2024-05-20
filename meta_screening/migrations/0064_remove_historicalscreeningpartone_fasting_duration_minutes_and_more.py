# Generated by Django 4.2.11 on 2024-05-16 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "meta_screening",
            "0063_alter_historicalscreeningpartone_fasting_duration_str_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalscreeningpartone",
            name="fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartone",
            name="repeat_fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartthree",
            name="fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartthree",
            name="repeat_fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningparttwo",
            name="fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningparttwo",
            name="repeat_fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicalsubjectscreening",
            name="fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="historicalsubjectscreening",
            name="repeat_fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="subjectscreening",
            name="fasting_duration_minutes",
        ),
        migrations.RemoveField(
            model_name="subjectscreening",
            name="repeat_fasting_duration_minutes",
        ),
        migrations.AddField(
            model_name="historicalscreeningpartone",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalscreeningpartone",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalscreeningpartthree",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalscreeningpartthree",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalscreeningparttwo",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalscreeningparttwo",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalsubjectscreening",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
        migrations.AddField(
            model_name="subjectscreening",
            name="repeat_fasting_duration_delta",
            field=models.DurationField(
                blank=True, help_text="system calculated value", null=True
            ),
        ),
    ]
