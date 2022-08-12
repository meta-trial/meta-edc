# Generated by Django 4.0.5 on 2022-06-28 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_screening", "0050_historicalscreeningpartone_agree_to_p3_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="advised_to_fast",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Not applicable if continuing to the second stage today",
                max_length=15,
                verbose_name="Has the patient been advised to return FASTED for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="agree_to_p3",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    (
                        "N/A",
                        "Not applicable, subject is not eligible based on the criteria above",
                    ),
                ],
                default="Yes",
                help_text="If patient is not continuing to the second stage today, advised to fast and provide a return appointment date below",
                max_length=15,
                verbose_name="Has the patient agreed to complete/return for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="appt_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Leave blank if continuing to the second stage today",
                null=True,
                verbose_name="Appointment date for second stage of screening (P3)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="p3_ltfu",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("N/A", "Decision pending / Not applicable")],
                default="N/A",
                help_text="Only applicable if the patient missed the appointment for the second stage of screening (P3), several attempts have been made to contact the patient, and the patient has not started P3. See above",
                max_length=15,
                verbose_name="Consider the patient 'lost to screening' for now?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="advised_to_fast",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Not applicable if continuing to the second stage today",
                max_length=15,
                verbose_name="Has the patient been advised to return FASTED for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="agree_to_p3",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    (
                        "N/A",
                        "Not applicable, subject is not eligible based on the criteria above",
                    ),
                ],
                default="Yes",
                help_text="If patient is not continuing to the second stage today, advised to fast and provide a return appointment date below",
                max_length=15,
                verbose_name="Has the patient agreed to complete/return for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="appt_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Leave blank if continuing to the second stage today",
                null=True,
                verbose_name="Appointment date for second stage of screening (P3)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="p3_ltfu",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("N/A", "Decision pending / Not applicable")],
                default="N/A",
                help_text="Only applicable if the patient missed the appointment for the second stage of screening (P3), several attempts have been made to contact the patient, and the patient has not started P3. See above",
                max_length=15,
                verbose_name="Consider the patient 'lost to screening' for now?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="advised_to_fast",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Not applicable if continuing to the second stage today",
                max_length=15,
                verbose_name="Has the patient been advised to return FASTED for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="agree_to_p3",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    (
                        "N/A",
                        "Not applicable, subject is not eligible based on the criteria above",
                    ),
                ],
                default="Yes",
                help_text="If patient is not continuing to the second stage today, advised to fast and provide a return appointment date below",
                max_length=15,
                verbose_name="Has the patient agreed to complete/return for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="appt_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Leave blank if continuing to the second stage today",
                null=True,
                verbose_name="Appointment date for second stage of screening (P3)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="p3_ltfu",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("N/A", "Decision pending / Not applicable")],
                default="N/A",
                help_text="Only applicable if the patient missed the appointment for the second stage of screening (P3), several attempts have been made to contact the patient, and the patient has not started P3. See above",
                max_length=15,
                verbose_name="Consider the patient 'lost to screening' for now?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="advised_to_fast",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Not applicable if continuing to the second stage today",
                max_length=15,
                verbose_name="Has the patient been advised to return FASTED for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="agree_to_p3",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    (
                        "N/A",
                        "Not applicable, subject is not eligible based on the criteria above",
                    ),
                ],
                default="Yes",
                help_text="If patient is not continuing to the second stage today, advised to fast and provide a return appointment date below",
                max_length=15,
                verbose_name="Has the patient agreed to complete/return for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="appt_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Leave blank if continuing to the second stage today",
                null=True,
                verbose_name="Appointment date for second stage of screening (P3)",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="p3_ltfu",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("N/A", "Decision pending / Not applicable")],
                default="N/A",
                help_text="Only applicable if the patient missed the appointment for the second stage of screening (P3), several attempts have been made to contact the patient, and the patient has not started P3. See above",
                max_length=15,
                verbose_name="Consider the patient 'lost to screening' for now?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="advised_to_fast",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                help_text="Not applicable if continuing to the second stage today",
                max_length=15,
                verbose_name="Has the patient been advised to return FASTED for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="agree_to_p3",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    (
                        "N/A",
                        "Not applicable, subject is not eligible based on the criteria above",
                    ),
                ],
                default="Yes",
                help_text="If patient is not continuing to the second stage today, advised to fast and provide a return appointment date below",
                max_length=15,
                verbose_name="Has the patient agreed to complete/return for the second stage of the screening?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="appt_datetime",
            field=models.DateTimeField(
                blank=True,
                help_text="Leave blank if continuing to the second stage today",
                null=True,
                verbose_name="Appointment date for second stage of screening (P3)",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="p3_ltfu",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("N/A", "Decision pending / Not applicable")],
                default="N/A",
                help_text="Only applicable if the patient missed the appointment for the second stage of screening (P3), several attempts have been made to contact the patient, and the patient has not started P3. See above",
                max_length=15,
                verbose_name="Consider the patient 'lost to screening' for now?",
            ),
        ),
    ]
