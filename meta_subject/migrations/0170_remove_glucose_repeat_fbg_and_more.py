# Generated by Django 5.0.1 on 2024-02-13 04:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("meta_subject", "0169_alter_dmreferralfollowup_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="glucose",
            name="repeat_fbg",
        ),
        migrations.RemoveField(
            model_name="historicalglucose",
            name="repeat_fbg",
        ),
        migrations.AlterField(
            model_name="glucose",
            name="endpoint_today",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("PENDING", "No. A repeat FBG will be scheduled"),
                    ("No", "No"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="Answer yes or no if both the FBG and OGTT are available",
                max_length=25,
                verbose_name="Has the participant reached a study endpoint today?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalglucose",
            name="endpoint_today",
            field=models.CharField(
                choices=[
                    ("Yes", "Yes"),
                    ("PENDING", "No. A repeat FBG will be scheduled"),
                    ("No", "No"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                help_text="Answer yes or no if both the FBG and OGTT are available",
                max_length=25,
                verbose_name="Has the participant reached a study endpoint today?",
            ),
        ),
    ]
