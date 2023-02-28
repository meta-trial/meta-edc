# Generated by Django 4.0.5 on 2022-06-29 17:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meta_subject", "0117_alter_egfrnotification_managers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="delivery",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default="COMPLETE",
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AddField(
            model_name="delivery",
            name="crf_status_comments",
            field=models.TextField(
                blank=True,
                help_text="for example, why some data is still pending",
                null=True,
                verbose_name="Any comments related to status of this CRF",
            ),
        ),
        migrations.AddField(
            model_name="historicaldelivery",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default="COMPLETE",
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AddField(
            model_name="historicaldelivery",
            name="crf_status_comments",
            field=models.TextField(
                blank=True,
                help_text="for example, why some data is still pending",
                null=True,
                verbose_name="Any comments related to status of this CRF",
            ),
        ),
    ]
