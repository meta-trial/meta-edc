# Generated by Django 5.1.2 on 2025-01-15 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_consent", "0028_historicalsubjectconsentv1ext_assessment_score_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalsubjectconsentv1ext",
            name="agrees_to_extension",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                help_text="See above for the definition of extended followup.",
                max_length=15,
                verbose_name="Does the participant give consent to extend clinic followup as per the protocol amendment?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectconsentv1ext",
            name="agrees_to_extension",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                help_text="See above for the definition of extended followup.",
                max_length=15,
                verbose_name="Does the participant give consent to extend clinic followup as per the protocol amendment?",
            ),
        ),
    ]
