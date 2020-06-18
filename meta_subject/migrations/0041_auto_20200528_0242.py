# Generated by Django 3.0.6 on 2020-05-27 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("meta_lists", "0007_auto_20200516_2356"),
        ("meta_subject", "0040_auto_20200527_2155"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalfollowup",
            name="art_new_regimen",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="meta_lists.ArvRegimens",
                verbose_name="Please indicate new regimen",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="admitted_hospital",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="If YES, were they admitted to hospital?",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="any_other_problems",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Since your last visit has the participant experienced any other medical or health problems NOT listed above",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="any_other_problems_detail",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If YES, please provide details of the event",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="any_other_problems_sae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Does this event constitute an Adverse Event?",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="art_change",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Since the participant's last visit has there been any change in their HIV medication?",
            ),
        ),
        migrations.RemoveField(model_name="followup", name="art_new_regimen",),
        migrations.AddField(
            model_name="followup",
            name="art_new_regimen",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="art_new_regimen",
                to="meta_lists.ArvRegimens",
                verbose_name="Please indicate new regimen",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="attended_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Includes other routine appointments, e.g. BP check or family planning",
                max_length=25,
                verbose_name="Since the participant's last visit did they attend any other clinic or hospital for care for any reason",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="attended_clinic_detail",
            field=models.TextField(
                blank=True,
                help_text="If the participant was given a referral letter or discharge summary record details here",
                null=True,
                verbose_name="If YES, attend other clinic or hospital, please provide details of this event",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="attended_clinic_sae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If YES, submit a <u>Serious Adverse Event</u> Form",
                max_length=25,
                verbose_name="Does the event constitute a <u>Serious Adverse Event</u>",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="hepatomegaly",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="This condition often does not have any clinical signs and symptoms, it may present with an enlarge liver on examination, and symptoms of fatigue and right upper abdominal pain. The risk of developing this condition is higher in patients who are obese and who have type 2 diabetes or metabolic syndrome",
                max_length=25,
                verbose_name="Do you think the participant has hepatomegaly with steatosis?",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="lactic_acidosis",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Classical signs of lactic acidosis include: abdominal or stomach discomfort, decreased appetite, diarrhoea, fast or shallow breathing, a general feeling of discomfort, muscle pain or cramping; and unusual sleepiness, fatigue, or weakness.",
                max_length=25,
                verbose_name="Do you think the participant has lactic acidosis?",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="prescribed_medication",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Was the participant prescribed any other medication at this clinic or hospital visit?",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="referral",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Is the participant being referred",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="symptoms",
            field=models.ManyToManyField(
                help_text="either at this hospital or at a different clinic",
                related_name="symptoms",
                to="meta_lists.Symptoms",
                verbose_name="Since the participant's last appointment have they experienced any of the following symptoms",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="symptoms_sought_care",
            field=models.ManyToManyField(
                related_name="symptoms_sought_care",
                to="meta_lists.Symptoms",
                verbose_name="Did they seek care from any health worker for these symptoms",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="admitted_hospital",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="If YES, were they admitted to hospital?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="any_other_problems",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Since your last visit has the participant experienced any other medical or health problems NOT listed above",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="any_other_problems_detail",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If YES, please provide details of the event",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="any_other_problems_sae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Does this event constitute an Adverse Event?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="art_change",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Since the participant's last visit has there been any change in their HIV medication?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="attended_clinic",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Includes other routine appointments, e.g. BP check or family planning",
                max_length=25,
                verbose_name="Since the participant's last visit did they attend any other clinic or hospital for care for any reason",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="attended_clinic_detail",
            field=models.TextField(
                blank=True,
                help_text="If the participant was given a referral letter or discharge summary record details here",
                null=True,
                verbose_name="If YES, attend other clinic or hospital, please provide details of this event",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="attended_clinic_sae",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="If YES, submit a <u>Serious Adverse Event</u> Form",
                max_length=25,
                verbose_name="Does the event constitute a <u>Serious Adverse Event</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="hepatomegaly",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="This condition often does not have any clinical signs and symptoms, it may present with an enlarge liver on examination, and symptoms of fatigue and right upper abdominal pain. The risk of developing this condition is higher in patients who are obese and who have type 2 diabetes or metabolic syndrome",
                max_length=25,
                verbose_name="Do you think the participant has hepatomegaly with steatosis?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="lactic_acidosis",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Classical signs of lactic acidosis include: abdominal or stomach discomfort, decreased appetite, diarrhoea, fast or shallow breathing, a general feeling of discomfort, muscle pain or cramping; and unusual sleepiness, fatigue, or weakness.",
                max_length=25,
                verbose_name="Do you think the participant has lactic acidosis?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="prescribed_medication",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Was the participant prescribed any other medication at this clinic or hospital visit?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="referral",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=25,
                verbose_name="Is the participant being referred",
            ),
        ),
    ]
