# Generated by Django 3.2.11 on 2022-03-04 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meta_screening", "0035_auto_20220304_2233"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="repeat_fasting",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="As reported by patient",
                max_length=15,
                null=True,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartone",
            name="repeat_glucose_performed",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="Were the glucose measurements repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="repeat_fasting",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="As reported by patient",
                max_length=15,
                null=True,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningpartthree",
            name="repeat_glucose_performed",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="Were the glucose measurements repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="repeat_fasting",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="As reported by patient",
                max_length=15,
                null=True,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalscreeningparttwo",
            name="repeat_glucose_performed",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="Were the glucose measurements repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="repeat_fasting",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="As reported by patient",
                max_length=15,
                null=True,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubjectscreening",
            name="repeat_glucose_performed",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="Were the glucose measurements repeated?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="repeat_fasting",
            field=models.CharField(
                blank=True,
                choices=[("Yes", "Yes"), ("No", "No")],
                help_text="As reported by patient",
                max_length=15,
                null=True,
                verbose_name="Has the participant fasted?",
            ),
        ),
        migrations.AlterField(
            model_name="subjectscreening",
            name="repeat_glucose_performed",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("No", "No"),
                    ("PENDING", "Pending"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="If repeated, must be at least 3 days after the first glucose measures (FBG, OGTT)",
                max_length=15,
                verbose_name="Were the glucose measurements repeated?",
            ),
        ),
    ]