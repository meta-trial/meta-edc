# Generated by Django 4.2.11 on 2024-08-01 16:48

from django.db import migrations, models
import edc_crf.model_mixins.crf_status_model_mixin


class Migration(migrations.Migration):

    dependencies = [
        ("meta_subject", "0207_alter_historicalphysicalexam_waist_circumference_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="birthoutcomes",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AddField(
            model_name="birthoutcomes",
            name="crf_status_comments",
            field=models.TextField(
                blank=True,
                help_text="for example, why some data is still pending",
                null=True,
                verbose_name="Any comments related to status of this CRF",
            ),
        ),
        migrations.AddField(
            model_name="historicalbirthoutcomes",
            name="crf_status",
            field=models.CharField(
                choices=[
                    ("INCOMPLETE", "Incomplete (some data pending)"),
                    ("COMPLETE", "Complete"),
                ],
                default=edc_crf.model_mixins.crf_status_model_mixin.get_crf_status_default,
                help_text="If some data is still pending, flag this CRF as incomplete",
                max_length=25,
                verbose_name="CRF status",
            ),
        ),
        migrations.AddField(
            model_name="historicalbirthoutcomes",
            name="crf_status_comments",
            field=models.TextField(
                blank=True,
                help_text="for example, why some data is still pending",
                null=True,
                verbose_name="Any comments related to status of this CRF",
            ),
        ),
    ]
