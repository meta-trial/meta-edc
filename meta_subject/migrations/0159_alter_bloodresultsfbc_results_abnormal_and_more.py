# Generated by Django 4.1.2 on 2023-03-01 18:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meta_subject", "0158_alter_followupexamination_attended_clinic_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodresultsfbc",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultsglu",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultshba1c",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultsins",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultslft",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultslipid",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="bloodresultsrft",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsfbc",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsglu",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultshba1c",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsins",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslft",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultslipid",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalbloodresultsrft",
            name="results_abnormal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="Abnormal results present at baseline or continuing from baseline not included.",
                max_length=25,
                verbose_name="Are any of the above results abnormal?",
            ),
        ),
    ]
