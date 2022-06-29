# Generated by Django 3.2.11 on 2022-04-03 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_screening", "0041_auto_20220403_1227"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicalscreeningpartone",
            name="fasting_opinion",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartone",
            name="fbg2_performed",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartone",
            name="ogtt2_performed",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartone",
            name="repeat_fasting_opinion",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartthree",
            name="fasting_opinion",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartthree",
            name="fbg2_performed",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartthree",
            name="ogtt2_performed",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningpartthree",
            name="repeat_fasting_opinion",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningparttwo",
            name="fasting_opinion",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningparttwo",
            name="fbg2_performed",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningparttwo",
            name="ogtt2_performed",
        ),
        migrations.RemoveField(
            model_name="historicalscreeningparttwo",
            name="repeat_fasting_opinion",
        ),
        migrations.RemoveField(
            model_name="historicalsubjectscreening",
            name="fasting_opinion",
        ),
        migrations.RemoveField(
            model_name="historicalsubjectscreening",
            name="fbg2_performed",
        ),
        migrations.RemoveField(
            model_name="historicalsubjectscreening",
            name="ogtt2_performed",
        ),
        migrations.RemoveField(
            model_name="historicalsubjectscreening",
            name="repeat_fasting_opinion",
        ),
        migrations.RemoveField(
            model_name="subjectscreening",
            name="fasting_opinion",
        ),
        migrations.RemoveField(
            model_name="subjectscreening",
            name="fbg2_performed",
        ),
        migrations.RemoveField(
            model_name="subjectscreening",
            name="ogtt2_performed",
        ),
        migrations.RemoveField(
            model_name="subjectscreening",
            name="repeat_fasting_opinion",
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="art_six_months",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Has the patient been on anti-retroviral therapy for <u>at least 6 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="meta_phase_two",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was the subject enrolled in the <u>META Phase 2</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="repeat_glucose_opinion",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="In opinion of the clinician, should the glucose measurements be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="screening_consent",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the subject given his/her verbal consent to be screened for the <u>META Phase 3</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="staying_nearby_12",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Is the patient planning to remain in the catchment area for <u>at least 12 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="vl_undetectable",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Does the patient have a viral load measure of less than 400 copies per ml taken <u>within the last 6 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="art_six_months",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Has the patient been on anti-retroviral therapy for <u>at least 6 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="meta_phase_two",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was the subject enrolled in the <u>META Phase 2</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="repeat_glucose_opinion",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="In opinion of the clinician, should the glucose measurements be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="screening_consent",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the subject given his/her verbal consent to be screened for the <u>META Phase 3</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="staying_nearby_12",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Is the patient planning to remain in the catchment area for <u>at least 12 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="vl_undetectable",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Does the patient have a viral load measure of less than 400 copies per ml taken <u>within the last 6 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="art_six_months",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Has the patient been on anti-retroviral therapy for <u>at least 6 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="meta_phase_two",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was the subject enrolled in the <u>META Phase 2</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="repeat_glucose_opinion",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="In opinion of the clinician, should the glucose measurements be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="screening_consent",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the subject given his/her verbal consent to be screened for the <u>META Phase 3</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="staying_nearby_12",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Is the patient planning to remain in the catchment area for <u>at least 12 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="vl_undetectable",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Does the patient have a viral load measure of less than 400 copies per ml taken <u>within the last 6 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="art_six_months",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Has the patient been on anti-retroviral therapy for <u>at least 6 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="meta_phase_two",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was the subject enrolled in the <u>META Phase 2</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="repeat_glucose_opinion",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="In opinion of the clinician, should the glucose measurements be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="screening_consent",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the subject given his/her verbal consent to be screened for the <u>META Phase 3</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="staying_nearby_12",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Is the patient planning to remain in the catchment area for <u>at least 12 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="vl_undetectable",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Does the patient have a viral load measure of less than 400 copies per ml taken <u>within the last 6 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="art_six_months",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Has the patient been on anti-retroviral therapy for <u>at least 6 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="meta_phase_two",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Was the subject enrolled in the <u>META Phase 2</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="repeat_glucose_opinion",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                default="No",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="In opinion of the clinician, should the glucose measurements be repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="screening_consent",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                verbose_name="Has the subject given his/her verbal consent to be screened for the <u>META Phase 3</u> trial?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="staying_nearby_12",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                max_length=15,
                null=True,
                verbose_name="Is the patient planning to remain in the catchment area for <u>at least 12 months</u>",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="vl_undetectable",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=15,
                verbose_name="Does the patient have a viral load measure of less than 400 copies per ml taken <u>within the last 6 months</u>",
            ),
        ),
    ]
