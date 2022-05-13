# Generated by Django 4.0.4 on 2022-05-12 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("edc_mnsi", "0003_alter_mnsi_abnormal_obs_left_foot_and_more"),
        ("meta_subject", "0110_auto_20220512_1811"),
    ]

    operations = [
        migrations.AlterField(
            model_name="followupvitals",
            name="severe_htn",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Based on the above readings. Severe HTN is any BP reading > 180/110mmHg",
                max_length=15,
                null=True,
                verbose_name="Does the patient have severe hypertension?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowupvitals",
            name="severe_htn",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Based on the above readings. Severe HTN is any BP reading > 180/110mmHg",
                max_length=15,
                null=True,
                verbose_name="Does the patient have severe hypertension?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="severe_htn",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Based on the above readings. Severe HTN is any BP reading > 180/110mmHg",
                max_length=15,
                null=True,
                verbose_name="Does the patient have severe hypertension?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="abnormal_obs_left_foot",
            field=models.ManyToManyField(
                blank=True,
                related_name="+",
                to="edc_mnsi.abnormalfootappearanceobservations",
                verbose_name="If NO, check all that apply to LEFT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="mnsi",
            name="abnormal_obs_right_foot",
            field=models.ManyToManyField(
                blank=True,
                related_name="+",
                to="edc_mnsi.abnormalfootappearanceobservations",
                verbose_name="If NO, check all that apply to RIGHT foot?",
            ),
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="severe_htn",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Based on the above readings. Severe HTN is any BP reading > 180/110mmHg",
                max_length=15,
                null=True,
                verbose_name="Does the patient have severe hypertension?",
            ),
        ),
    ]
