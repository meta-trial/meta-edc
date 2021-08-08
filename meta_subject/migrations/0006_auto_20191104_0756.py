# Generated by Django 2.2.6 on 2019-11-04 04:56

import django.core.validators
import django.db.models.deletion
import edc_model_fields.fields.other_charfield
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_lists", "0004_auto_20191102_1859"),
        ("meta_subject", "0005_auto_20191024_1000"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalpatienthistory",
            old_name="hypertension",
            new_name="hypertension_diagnosis",
        ),
        migrations.RenameField(
            model_name="historicalpatienthistory",
            old_name="statins",
            new_name="taking_statins",
        ),
        migrations.RenameField(
            model_name="patienthistory",
            old_name="hypertension",
            new_name="hypertension_diagnosis",
        ),
        migrations.RenameField(
            model_name="patienthistory", old_name="statins", new_name="taking_statins"
        ),
        migrations.RemoveField(
            model_name="historicalmedicationadherence", name="missed_pill_reason"
        ),
        migrations.RemoveField(
            model_name="historicalmedicationadherence", name="visual_score"
        ),
        migrations.RemoveField(
            model_name="historicalpatienthistory", name="family_diabetics"
        ),
        migrations.RemoveField(
            model_name="historicalpatienthistory", name="htn_treatment"
        ),
        migrations.RemoveField(
            model_name="historicalpatienthistory", name="other_past_year_symptoms"
        ),
        migrations.RemoveField(
            model_name="historicalphysicalexam", name="has_abdominal_tenderness"
        ),
        migrations.RemoveField(
            model_name="historicalphysicalexam", name="has_enlarged_liver"
        ),
        migrations.RemoveField(
            model_name="historicalphysicalexam", name="is_heartbeat_regular"
        ),
        migrations.RemoveField(model_name="medicationadherence", name="visual_score"),
        migrations.RemoveField(model_name="patienthistory", name="family_diabetics"),
        migrations.RemoveField(
            model_name="patienthistory", name="other_past_year_symptoms"
        ),
        migrations.RemoveField(
            model_name="physicalexam", name="has_abdominal_tenderness"
        ),
        migrations.RemoveField(model_name="physicalexam", name="has_enlarged_liver"),
        migrations.RemoveField(model_name="physicalexam", name="is_heartbeat_regular"),
        migrations.AddField(
            model_name="historicalmedicationadherence",
            name="other_missed_pill_reason",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalmedicationadherence",
            name="visual_score_confirmed",
            field=models.IntegerField(
                default=0,
                help_text="%",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="<B><font color='orange'>Interviewer</font></B>: please confirm the score indicated from above.",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalmedicationadherence",
            name="visual_score_slider",
            field=models.CharField(
                default="0", help_text="%", max_length=3, verbose_name="Visual score"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalpatienthistory",
            name="dm_in_family",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="?",
                help_text="Immediate family is parents, siblings, and children",
                max_length=15,
                verbose_name="Has anyone in your immediate family ever been diagnosed with diabetes?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalpatienthistory",
            name="other_dm_symptoms",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other symptom in the <u>past year</u>, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalpatienthistory",
            name="other_htn_treatment",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other medication(s), please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="historicalphysicalexam",
            name="abdominal_tenderness_description",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If YES, abdominal tenderness, please describe",
            ),
        ),
        migrations.AddField(
            model_name="historicalphysicalexam",
            name="enlarged_liver",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="?",
                max_length=15,
                verbose_name="Enlarged liver on palpation?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalphysicalexam",
            name="irregular_heartbeat_description",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If the heartbeat is <u>irregular</u>, please describe",
            ),
        ),
        migrations.AddField(
            model_name="medicationadherence",
            name="other_missed_pill_reason",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="medicationadherence",
            name="visual_score_confirmed",
            field=models.IntegerField(
                default=0,
                help_text="%",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
                verbose_name="<B><font color='orange'>Interviewer</font></B>: please confirm the score indicated from above.",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="medicationadherence",
            name="visual_score_slider",
            field=models.CharField(
                default="0", help_text="%", max_length=3, verbose_name="Visual score"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="patienthistory",
            name="dm_in_family",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="?",
                help_text="Immediate family is parents, siblings, and children",
                max_length=15,
                verbose_name="Has anyone in your immediate family ever been diagnosed with diabetes?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="patienthistory",
            name="other_dm_symptoms",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other symptom in the <u>past year</u>, please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="patienthistory",
            name="other_htn_treatment",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other medication(s), please specify ...",
            ),
        ),
        migrations.AddField(
            model_name="physicalexam",
            name="abdominal_tenderness_description",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If YES, abdominal tenderness, please describe",
            ),
        ),
        migrations.AddField(
            model_name="physicalexam",
            name="enlarged_liver",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="?",
                max_length=15,
                verbose_name="Enlarged liver on palpation?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="physicalexam",
            name="irregular_heartbeat_description",
            field=models.TextField(
                blank=True,
                null=True,
                verbose_name="If the heartbeat is <u>irregular</u>, please describe",
            ),
        ),
        migrations.AlterField(
            model_name="followup",
            name="art_new_regimen_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalfollowup",
            name="art_new_regimen_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="current_smoker",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Is the patient a <u>current</u> smoker?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="former_smoker",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient a <u>previous</u> smoker?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="other_current_arv_regimen",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="other_oi_prophylaxis",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="other_previous_arv_regimen",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatienthistory",
            name="other_symptoms",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="abdominal_tenderness",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="?",
                max_length=15,
                verbose_name="Abdominal tenderness on palpation?",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="irregular_heartbeat",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="?",
                max_length=15,
                verbose_name="Is the heart beat <u>irregular</u>?",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="jaundice",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Jaundice?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalphysicalexam",
            name="peripheral_oedema",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Presence of peripheral oedema?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectrequisition",
            name="reason_not_drawn_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.RemoveField(
            model_name="medicationadherence", name="missed_pill_reason"
        ),
        migrations.AddField(
            model_name="medicationadherence",
            name="missed_pill_reason",
            field=models.ManyToManyField(
                blank=True,
                to="meta_lists.NonAdherenceReasons",
                verbose_name="Reasons for missing study pills",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="current_smoker",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Is the patient a <u>current</u> smoker?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="dm_symptoms",
            field=models.ManyToManyField(
                to="meta_lists.DiabetesSymptoms",
                verbose_name="In the <u>past year</u>, have you had any of the following symptoms?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="former_smoker",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=15,
                verbose_name="Is the patient a <u>previous</u> smoker?",
            ),
        ),
        migrations.RemoveField(model_name="patienthistory", name="htn_treatment"),
        migrations.AddField(
            model_name="patienthistory",
            name="htn_treatment",
            field=models.ManyToManyField(
                blank=True,
                to="meta_lists.HypertensionMedications",
                verbose_name="What medications is the patient currently taking for hypertension?",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="other_current_arv_regimen",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="other_oi_prophylaxis",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="other_previous_arv_regimen",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="other_symptoms",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
        migrations.AlterField(
            model_name="patienthistory",
            name="previous_arv_regimen",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="previous_arv_regimen",
                to="meta_lists.ArvRegimens",
                verbose_name="Which antiretroviral therapy regimen was the patient previously on?",
            ),
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="abdominal_tenderness",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="?",
                max_length=15,
                verbose_name="Abdominal tenderness on palpation?",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="irregular_heartbeat",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="?",
                max_length=15,
                verbose_name="Is the heart beat <u>irregular</u>?",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="jaundice",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Jaundice?",
            ),
        ),
        migrations.AlterField(
            model_name="physicalexam",
            name="peripheral_oedema",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Presence of peripheral oedema?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectrequisition",
            name="reason_not_drawn_other",
            field=edc_model_fields.fields.other_charfield.OtherCharField(
                blank=True,
                max_length=35,
                null=True,
                verbose_name="If other, please specify ...",
            ),
        ),
    ]
